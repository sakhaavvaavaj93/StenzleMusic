from hydrogram import filters
from hydrogram.types import Message
from StenzleMusic import app, pytgcalls
from StenzleMusic.Helpers import admin_check, close_key, is_streaming, stream_off


@app.on_message(filters.command(["pause"]) & filters.group)
@admin_check
async def pause_str(_, message: Message):
    try:
        await message.delete()
    except:
        pass

    if not await is_streaming(message.chat.id):
        return await message.reply_text(
            "ᴅɪᴅ ʏᴏᴜ ʀᴇᴍᴇᴍʙᴇʀ ᴛʜᴀᴛ ʏᴏᴜ ʀᴇsᴜᴍᴇᴅ ᴛʜᴇ sᴛʀᴇᴀᴍ ?"
        )

    await pytgcalls.pause_stream(message.chat.id)
    await stream_off(message.chat.id)
    
