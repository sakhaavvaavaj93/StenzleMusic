import asyncio
import importlib
import os
import threading
from flask import Flask
from hydrogram import idle
from StenzleMusic import (
    ASS_ID, ASS_NAME, ASS_USERNAME,
    BOT_ID, BOT_NAME, BOT_USERNAME,
    LOGGER, app, app2, pytgcalls,
)
from StenzleMusic.Modules import ALL_MODULES

# --- Flask Web Server for Render ---
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return "StenzleMusic is running!"

def run_web():
    # Render uses port 10000 by default
    web_app.run(host="0.0.0.0", port=10000)

# Start web server in background thread
threading.Thread(target=run_web, daemon=True).start()

# --- Main Startup Logic ---
async def Stenzle_startup():
    # 1. Start Telegram Clients First
    LOGGER.info("[•] Starting Clients...")
    await app.start()
    await app2.start()
    
    # 2. Start PyTgCalls (The music engine)
    LOGGER.info("[•] Starting PyTgCalls Client...")
    await pytgcalls.start()

    # 3. Load Modules (Commands) AFTER clients are online
    LOGGER.info("[•] Loading Modules...")
    for module in ALL_MODULES:
        importlib.import_module("StenzleMusic.Modules." + module)
    LOGGER.info(f"[•] Loaded {len(ALL_MODULES)} Modules.")

    # 4. Refresh Directories
    LOGGER.info("[•] Refreshing Directories...")
    if not os.path.exists("downloads"):
        os.mkdir("downloads")
    if not os.path.exists("cache"):
        os.mkdir("cache")

    # 5. Finalize
    LOGGER.info(f"[•] Bot Started As {BOT_NAME}.")
    LOGGER.info(f"[•] Assistant Started As {ASS_NAME}.")
    
    # Optional: Send a notification that bot is live
    try:
        await app2.send_message(BOT_USERNAME, "/start")
    except:
        pass

    # Keeps the bot running
    await idle()
    
    # Cleanup on exit
    await app.stop()
    await app2.stop()

if __name__ == "__main__":
    try:
        asyncio.run(Stenzle_startup())
    except KeyboardInterrupt:
        LOGGER.info("Bot stopped manually.")
    except Exception as e:
        LOGGER.error(f"Fatal error during startup: {e}")
