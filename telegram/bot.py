import os
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

async def start(update, context):
    await update.message.reply_text('HNPE Bot active')

if __name__ == '__main__':
    if not TOKEN:
        print('TELEGRAM_BOT_TOKEN not set; exiting.')
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.run_polling()
