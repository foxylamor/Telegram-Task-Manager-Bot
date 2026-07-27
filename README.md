# Telegram Task Manager Bot

Telegram bot for managing personal tasks. Users can add, view, mark as done, and delete tasks with simple commands.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![aiogram](https://img.shields.io/badge/aiogram-v3.0%2B-blue?style=for-the-badge&logo=telegram)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
  <img src="https://i.ibb.co/QLz2gpv/photo-2026-05-30-18-40-19.jpg" width="250" alt="Demo of bot">
  <img src="https://i.ibb.co/nq1909zs/photo-2026-05-30-18-40-21-2.jpg" width="250" alt="Demo of bot">
  <img src="https://i.ibb.co/nq1909zs/photo-2026-05-30-18-40-21-2.jpg" width="250" alt="Demo of bot">
</div>

## 🛠️ Tech Stack

- **aiogram** — modern asynchronous framework for Telegram bots
- **aiosqlite** — async SQLite database driver
- **python-dotenv** — environment variable management

## 📁 Project structure

```
telegram-task-manager-bot/
├── handlers/
│   └── routes.py        # Command handlers and routing logic
├── middleware/
│   └── rate_limit.py    # Rate limiting middleware (if implemented)
├── db.py                # Database operations (SQLite)
├── bot.py               # Main bot file with dispatcher setup
└── requirements.txt     # Project dependencies
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/foxylamor/telegram-task-manager-bot.git
cd telegram-task-manager-bot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
TOKEN=your_telegram_token_from_botfather
```

> 💡 **How to get a token?**
> 1. Open Telegram and find the **@BotFather** bot
> 2. Send the `/newbot` command
> 3. Follow the instructions and copy your token

### 5. Run the bot

```bash
python bot.py
```

## 📱 Usage

1. Open Telegram and find your bot
2. Send `/start` to initialize
3. Use commands:
   - `/add <description>` — add a new task (the bot will ask if you want a reminder and after how many minutes)
   - `/tasks` — view your tasks with numbers
   - `/done <number>` — mark task as done
   - `/delete <number>` — delete a task


## 📖 Documentation

- [aiogram](https://docs.aiogram.dev/)
- [aiosqlite](https://aiosqlite.omnilib.dev/)
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
