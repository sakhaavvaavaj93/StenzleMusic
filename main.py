import asyncio
import importlib
import os
from pyrogram import idle
from StenzleMusic import (
    ASS_ID, ASS_NAME, ASS_USERNAME,
    BOT_ID, BOT_NAME, BOT_USERNAME,
    LOGGER, SUNAME, app, app2, pytgcalls,
)
from StenzleMusic.Modules import ALL_MODULES

async def Stenzle_startup():
    LOGGER.info("[•] Loading Modules...")
    for module in ALL_MODULES:
        importlib.import_module("StenzleMusic.Modules." + module)
    LOGGER.info(f"[•] Loaded {len(ALL_MODULES)} Modules.")

    LOGGER.info("[•] Refreshing Directories...")
    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    if "cache" not in os.listdir():
        os.mkdir("cache")
    
    # Ensure clients are started before sending messages
    await app.start()
    await app2.start()
    
    await app2.send_message(BOT_USERNAME, "/start")

    LOGGER.info(f"[•] Bot Started As {BOT_NAME}.")
    LOGGER.info(f"[•] Assistant Started As {ASS_NAME}.")

    LOGGER.info("[•] Starting PyTgCalls Client...")
    await pytgcalls.start()
    
    # idle() keeps the bot running until interrupted
    await idle()
    
    # Proper shutdown
    await app.stop()
    await app2.stop()

if __name__ == "__main__":
    try:
        # asyncio.run is the ONLY safe way to start the loop in Python 3.14
        asyncio.run(Stenzle_startup())
    except KeyboardInterrupt:
        LOGGER.info("Bot stopped manually.")
    except Exception as e:
        LOGGER.error(f"Fatal error during startup: {e}")
