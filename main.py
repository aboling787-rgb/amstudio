from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from commands import start_command, help_command, handle_audio
from config import BOT_TOKEN, MAX_FILE_SIZE_MB
import os

if not os.path.exists('downloads'):
    os.makedirs('downloads')

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.bot_data['max_file_size'] = MAX_FILE_SIZE_MB

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.document.audio, handle_audio))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()