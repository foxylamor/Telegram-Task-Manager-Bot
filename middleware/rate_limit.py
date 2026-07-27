import time

from aiogram import BaseMiddleware

class RateLimitMiddleware(BaseMiddleware):
    """Middleware to implement rate limiting for handlers."""
    def __init__(self, limit: int = 3) -> None:
        super().__init__()
        self.limit = limit
        self.user_timestamps = {}

    async def __call__(self, handler, event, data) -> None:
        user_id = event.from_user.id
        current_time = time.time()

        if user_id in self.user_timestamps:
            elapsed_time = current_time - self.user_timestamps[user_id]
            if elapsed_time < self.limit:
                await event.answer(f"Please wait {int(self.limit - elapsed_time)} seconds before sending another command.")
                return

        self.user_timestamps[user_id] = current_time
        return await handler(event, data)