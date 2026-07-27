import asyncio

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from db import add_task, get_tasks, get_task_id_by_index, mark_task_done, delete_task, get_due_reminders, mark_reminder_sent


router = Router()


class AddTaskStates(StatesGroup):
    description = State()
    reminder_confirm = State()
    reminder_minutes = State()


@router.message(F.text == "/start")
async def start_handler(message: Message) -> None:
    """Handler for the /start command."""
    await message.answer("Hello! I'm your task manager bot. You can add tasks by sending me a message, and I'll keep track of them for you.\n\nCommands:\n/add <task description> - Add a new task\n/tasks - List all your tasks\n/done <task number> - Mark a task as done\n/delete <task number> - Delete a task")


@router.message(F.text.startswith("/add"))
async def add_task_handler(message: Message, state: FSMContext) -> None:
    """Handler for adding a new task."""
    description = message.text[4:].strip()
    if not description:
        await message.answer("Please provide a task description after the /add command. Example: /add Buy groceries")
        return

    await state.update_data(description=description)
    await state.set_state(AddTaskStates.reminder_confirm)
    await message.answer("Do you want a reminder for this task? Reply with yes or no.")


@router.message(AddTaskStates.reminder_confirm)
async def add_task_reminder_confirm(message: Message, state: FSMContext) -> None:
    answer = message.text.strip().lower()
    if answer in {"no", "n"}:
        data = await state.get_data()
        description = data.get("description")
        await add_task(message.from_user.id, description)
        await message.answer(f"Task added: {description}")
        await state.clear()
        return

    if answer in {"yes", "y"}:
        await state.set_state(AddTaskStates.reminder_minutes)
        await message.answer("How many minutes from now should I remind you? Please send a number.")
        return

    await message.answer("Please answer with yes or no.")


@router.message(AddTaskStates.reminder_minutes)
async def add_task_reminder_minutes(message: Message, state: FSMContext) -> None:
    try:
        minutes = int(message.text.strip())
    except ValueError:
        await message.answer("Please enter a valid number of minutes.")
        return

    if minutes <= 0:
        await message.answer("Please enter a positive number of minutes.")
        return

    data = await state.get_data()
    description = data.get("description")
    await add_task(message.from_user.id, description, reminder_requested=True, reminder_minutes=minutes)
    await message.answer(f"Task added with reminder in {minutes} minutes: {description}")
    await state.clear()


@router.message(F.text == "/tasks")
async def list_tasks_handler(message: Message) -> None:
    """Handler for listing all tasks."""
    tasks = await get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("You have no tasks.")
        return

    response = "Your tasks:\n"
    for index, (_, description, is_done) in enumerate(tasks, start=1):
        status = "✅" if is_done else "❌"
        response += f"{index}. {status} {description}\n"

    response += "\nUse /done <number> or /delete <number>."
    await message.answer(response)


@router.message(F.text.startswith("/done"))
async def mark_task_done_handler(message: Message) -> None:
    """Handler for marking a task as done by user-specific task number."""
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip():
        await message.answer("Please provide a task number after the /done command. Example: /done 1")
        return

    try:
        task_index = int(args[1].strip())
    except ValueError:
        await message.answer("Please provide a valid task number after the /done command. Example: /done 1")
        return

    task_id = await get_task_id_by_index(message.from_user.id, task_index)
    if task_id is None:
        await message.answer("Task number not found. Use /tasks to see your task numbers. Example: /done 1")
        return

    await mark_task_done(task_id)
    await message.answer(f"Task #{task_index} marked as done.")


@router.message(F.text.startswith("/delete"))
async def delete_task_handler(message: Message) -> None:
    """Handler for deleting a task by user-specific task number."""
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip():
        await message.answer("Please provide a task number after the /delete command. Example: /delete 1")
        return

    try:
        task_index = int(args[1].strip())
    except ValueError:
        await message.answer("Please provide a valid task number after the /delete command. Example: /delete 1")
        return

    task_id = await get_task_id_by_index(message.from_user.id, task_index)
    if task_id is None:
        await message.answer("Task number not found. Use /tasks to see your task numbers. Example: /delete 1")
        return

    await delete_task(task_id)
    await message.answer(f"Task #{task_index} has been deleted.")


async def reminder_worker(bot: Bot) -> None:
    """Background worker that sends reminders when tasks become due."""
    while True:
        due_tasks = await get_due_reminders()
        for task_id, user_id, description in due_tasks:
            try:
                await bot.send_message(user_id, f"⏰ Reminder: {description}")
                await mark_reminder_sent(task_id)
            except Exception:
                # Ignore send failures and try again later if needed
                pass

        await asyncio.sleep(60)
