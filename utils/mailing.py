import asyncio
from datetime import datetime

import pytz

from loader import db, bot


async def mailing(date, time, text):
    while True:
        if datetime.now(pytz.timezone('Europe/Moscow')).date().strftime('%Y-%m-%d') == date:
            if datetime.now(pytz.timezone('Europe/Moscow')).time().strftime('%H:%M') == time:
                users = await db.get_users()
                for user in users:
                    await bot.send_message(user[0], text)
                return
            else:
                await asyncio.sleep(60)
        else:
            await asyncio.sleep(60)
