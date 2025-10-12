from telegram import Bot
import os

BOT = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN', ''))

def send_signal_message(chat_id: str, text: str):
    if not BOT.token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not configured")
    return BOT.send_message(chat_id=chat_id, text=text)
