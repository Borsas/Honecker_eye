import os
import datetime
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext
import subprocess
from src.utils.env import DEVICE, CHANNEL_ID, GROUP_ID, IMAGE_CHAT_ID

async def update_picture(context: CallbackContext):
    image_path = get_image()
    photo = open(image_path, 'rb')

    await context.bot.edit_message_media(chat_id=CHANNEL_ID, message_id=IMAGE_CHAT_ID, media=InputMediaPhoto(media=photo))
    
    date = datetime.datetime.now().strftime("%d.%m.%Y. klo %H:%M:%S")
    msg = "Kuva päivitetty {date}".format(date=date)
    await context.bot.edit_message_caption(chat_id=CHANNEL_ID, message_id=IMAGE_CHAT_ID, caption=msg)
    os.remove(image_path)

async def send_picture(update: Update, context: CallbackContext):
    image_path = get_image()
    photo = open(image_path, 'rb')
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo)
    os.remove(image_path)


def get_image():
    if not os.path.exists("img/"):
        os.mkdir("img")
    image_name = "img/"+ datetime.datetime.now().isoformat() + ".jpg"
    CMD = "fswebcam -d {device} -r 1280x720 --jpeg 85 --no-banner --skip 120 --set exposure_auto=1 ./{image}".format(image=image_name, device=DEVICE).split(" ")

    subprocess.run(CMD)
    return image_name

