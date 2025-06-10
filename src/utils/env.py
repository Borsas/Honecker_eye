import os
from dotenv import load_dotenv
load_dotenv()

DEVICE = os.getenv("DEVICE_PATH")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GROUP_ID = os.getenv("GROUP_ID")
IMAGE_CHAT_ID = os.getenv("IMAGE_CHAT_ID")
