import os
import asyncio
from telegram import Update, error
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ChatJoinRequestHandler, CallbackContext
from dotenv import load_dotenv
from src.handlers import cameraHandler, registerHandler
from src.utils.env import DEVICE


def main():
    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    if os.path.exists(DEVICE) == False:
        print("No camera {camera} found. Exiting...".format(camera=DEVICE))
        return

    app = ApplicationBuilder().token(API_KEY).build()


    app.add_handler(CommandHandler("register", registerHandler.register))

    app.add_handler(CommandHandler("picture", cameraHandler.send_picture))

    job_queue = app.job_queue
    job_queue.run_repeating(cameraHandler.update_picture,  interval=5*60, first=1)
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()

