import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import ar  # Бібліотека для API Brawl Stars

load_dotenv()

# Завантаження токенів з .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
BRAWL_API_TOKEN = os.getenv("BRAWL_API_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
POST_ID = int(os.getenv("POST_ID"))

# Список клубів
CLUBS = {
    "KT the champion": "2RPOCQJ92",
    "KT Academy": "2YCP2QRL9",
    "KT Trailblazers": "2JJ8YVJGC",
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

# Ініціалізація клієнта Brawl Stars API
client = ar.Client(BRAWL_API_TOKEN)

async def get_club_info(club_tag):
    """Отримання даних клубу"""
    try:
        club = await client.get_club(club_tag)
        return {
            "name": club.name,
            "trophies": club.trophies,
            "requiredTrophies": club.required_trophies,
        }
    except ar.errors.RequestError as e:
        logging.error(f"Помилка отримання даних: {e}")
        return None

async def update_post():
    """Оновлення поста в Telegram-каналі"""
    message = "😎Вітаємо в імперії клубів КТ!\nМи входимо до гільдії Sun Guild☀️!\n\nНаші клуби:\n"
    for club_name, club_tag in CLUBS.items():
        info = await get_club_info(club_tag)
        if info:
            message += f"🟦{club_name} ({club_tag})\n🏆{info['trophies']}\n🏆{info['requiredTrophies']}+\n💬ТГ Чат: @KT_the_champion\n\n"
    
    await bot.edit_message_text(chat_id=CHANNEL_ID, message_id=POST_ID, text=message)
    logging.info("Пост оновлено!")

async def main():
    """Запуск бота"""
    scheduler.add_job(update_post, "interval", hours=1)
    scheduler.start()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
