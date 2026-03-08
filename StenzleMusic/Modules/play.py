import asyncio
import os
from hydrogram import filters
from hydrogram.enums import ChatMemberStatus
from hydrogram.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
# REMOVED: UnMuteNeeded (no longer exists in v2.0+)
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types import MediaStream, AudioQuality
from youtube_search import YoutubeSearch
from config import DURATION_LIMIT
from StenzleMusic import (
    ASS_ID,
    ASS_MENTION,
    ASS_NAME,
    ASS_USERNAME,
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    app,
    app2,
    Stenzledb,
    pytgcalls,
)
from StenzleMusic.Helpers.active import add_active_chat, is_active_chat, stream_on
from StenzleMusic.Helpers.downloaders import audio_dl
from StenzleMusic.Helpers.errors import DurationLimitError
from StenzleMusic.Helpers.gets import get_file_name, get_url
from StenzleMusic.Helpers.inline import buttons
from StenzleMusic.Helpers.queue import put
from StenzleMusic.Helpers.thumbnails import gen_qthumb, gen_thumb


@app.on_message(
    filters.command(["play", "p"])
    & filters.group
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    Stenzle = await message.reply_text("» ᴘʀᴏᴄᴇssɪɴɢ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")
    try:
        await message.delete()
    except:
        pass

    try:
        try:
            get = await app.get_chat_member(message.chat.id, ASS_ID)
        except ChatAdminRequired:
            return await Stenzle.edit_text(
                f"» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ ғᴏʀ ɪɴᴠɪᴛɪɴɢ {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴛᴏ {message.chat.title}."
            )
        if get.status == ChatMemberStatus.BANNED:
            unban_butt = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"ᴜɴʙᴀɴ {ASS_NAME}",
                            callback_data=f"unban_assistant {message.chat.id}|{ASS_ID}",
                        ),
                    ]
                ]
            )
            return await Stenzle.edit_text(
                text=f"» {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴɴᴇᴅ ɪɴ {message.chat.title}\n\n𖢵 ɪᴅ : `{ASS_ID}`\n𖢵 ɴᴀᴍᴇ : {ASS_MENTION}\n𖢵 ᴜsᴇʀɴᴀᴍᴇ : @{ASS_USERNAME}\n\nᴘʟᴇᴀsᴇ ᴜɴʙᴀɴ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴀɴᴅ ᴘʟᴀʏ ᴀɢᴀɪɴ...",
                reply_markup=unban_butt,
            )
    except UserNotParticipant:
        if message.chat.username:
            invitelink = message.chat.username
            try:
                await app2.resolve_peer(invitelink)
            except Exception as ex:
                LOGGER.error(ex)
        else:
            try:
                invitelink = await app.export_chat_invite_link(message.chat.id)
            except ChatAdminRequired:
                return await Stenzle.edit_text(
                    f"» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ ғᴏʀ ɪɴᴠɪᴛɪɴɢ {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴛᴏ {message.chat.title}."
                )
            except Exception as ex:
                return await Stenzle.edit_text(
                    f"ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴛᴏ {message.chat.title}.\n\n**ʀᴇᴀsᴏɴ :** `{ex}`"
                )
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
        anon = await Stenzle.edit_text(
            f"ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...\n\nɪɴᴠɪᴛɪɴɢ {ASS_NAME} ᴛᴏ {message.chat.title}."
        )
        try:
            await app2.join_chat(invitelink)
            await asyncio.sleep(2)
            await Stenzle.edit_text(
                f"{ASS_NAME} ᴊᴏɪɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ,\n\nsᴛᴀʀᴛɪɴɢ sᴛʀᴇᴀᴍ..."
            )
        except UserAlreadyParticipant:
            pass
        except Exception as ex:
            return await Stenzle.edit_text(
                f"ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴛᴏ {message.chat.title}.\n\n**ʀᴇᴀsᴏɴ :** `{ex}`"
            )
        try:
            await app2.resolve_peer(invitelink)
        except:
            pass

    ruser = message.from_user.first_name
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"» sᴏʀʀʏ ʙᴀʙʏ, ᴛʀᴀᴄᴋ ʟᴏɴɢᴇʀ ᴛʜᴀɴ  {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ᴏɴ {BOT_NAME}."
            )

        file_name = get_file_name(audio)
        title = file_name
        duration = round(audio.duration / 60)
        file_path = (
            await message.reply_to_message.download(file_name)
            if not os.path.isfile(os.path.join("downloads", file_name))
            else f"downloads/{file_name}"
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            title = results[0]["title"]
            duration = results[0]["duration"]
            videoid = results[0]["id"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            return await Stenzle.edit_text(f"sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ\n\n**ᴇʀʀᴏʀ :** `{e}`")

        if (dur / 60) > DURATION_LIMIT:
            return await Stenzle.edit_text(
                f"» sᴏʀʀʏ ʙᴀʙʏ, ᴛʀᴀᴄᴋ ʟᴏɴɢᴇʀ ᴛʜᴀɴ  {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ᴏɴ {BOT_NAME}."
            )
        file_path = audio_dl(url)
    else:
        if len(message.command) < 2:
            return await Stenzle.edit_text("» ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴɴᴀ ᴘʟᴀʏ ʙᴀʙʏ ?")
        query = message.text.split(None, 1)[1]
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            videoid = results[0]["id"]
            duration = results[0]["duration"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            LOGGER.error(str(e))
            return await Stenzle.edit("» ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ᴏ̨ᴜᴇʀʏ, ᴛʀʏ ᴘʟᴀʏɪɴɢ ᴀɢᴀɪɴ...")

        if (dur / 60) > DURATION_LIMIT:
            return await Stenzle.edit(
                f"» sᴏʀʀʏ ʙᴀʙʏ, ᴛʀᴀᴄᴋ ʟᴏɴɢᴇʀ ᴛʜᴀɴ  {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ᴏɴ {BOT_NAME}."
            )
        file_path = audio_dl(url)

    try:
        videoid = videoid
    except:
        videoid = "fuckitstgaudio"
        
    if await is_active_chat(message.chat.id):
        await put(
            message.chat.id,
            title,
            duration,
            videoid,
            file_path,
            ruser,
            message.from_user.id,
        )
    else:
        stream = MediaStream(file_path, audio_quality=AudioQuality.STUDIO)
        try:
            await pytgcalls.join_group_call(
                message.chat.id,
                stream,
            )
        except NoActiveGroupCall:
            return await Stenzle.edit_text(
                "**» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ ғᴏᴜɴᴅ.**\n\nᴩʟᴇᴀsᴇ ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ."
            )
        # Note: UnMuteNeeded block is removed as it's no longer a distinct importable exception
        
        await stream_on(message.chat.id)
        await add_active_chat(message.chat.id)
        
    return await Stenzle.delete()

@app.on_message(
    filters.command(["play", "p"])
    & filters.group
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    Stenzle = await message.reply_text("» ᴘʀᴏᴄᴇssɪɴɢ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")
    try:
        await message.delete()
    except:
        pass

    try:
        try:
            get = await app.get_chat_member(message.chat.id, ASS_ID)
        except ChatAdminRequired:
            return await Stenzle.edit_text(
                f"» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ ғᴏʀ ɪɴᴠɪᴛɪɴɢ {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴛᴏ {message.chat.title}."
            )
        if get.status == ChatMemberStatus.BANNED:
            unban_butt = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"ᴜɴʙᴀɴ {ASS_NAME}",
                            callback_data=f"unban_assistant {message.chat.id}|{ASS_ID}",
                        ),
                    ]
                ]
            )
            return await Stenzle.edit_text(
                text=f"» {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴɴᴇᴅ ɪɴ {message.chat.title}\n\n𖢵 ɪᴅ : `{ASS_ID}`\n𖢵 ɴᴀᴍᴇ : {ASS_MENTION}\n𖢵 ᴜsᴇʀɴᴀᴍᴇ : @{ASS_USERNAME}\n\nᴘʟᴇᴀsᴇ ᴜɴʙᴀɴ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴀɴᴅ ᴘʟᴀʏ ᴀɢᴀɪɴ...",
                reply_markup=unban_butt,
            )
    except UserNotParticipant:
        if message.chat.username:
            invitelink = message.chat.username
            try:
                await app2.resolve_peer(invitelink)
            except Exception as ex:
                LOGGER.error(ex)
        else:
            try:
                invitelink = await app.export_chat_invite_link(message.chat.id)
            except ChatAdminRequired:
                return await Stenzle.edit_text(
                    f"» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ ғᴏʀ ɪɴᴠɪᴛɪɴɢ {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴛᴏ {message.chat.title}."
                )
            except Exception as ex:
                return await Stenzle.edit_text(
                    f"ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴛᴏ {message.chat.title}.\n\n**ʀᴇᴀsᴏɴ :** `{ex}`"
                )
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
        anon = await Stenzle.edit_text(
            f"ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...\n\nɪɴᴠɪᴛɪɴɢ {ASS_NAME} ᴛᴏ {message.chat.title}."
        )
        try:
            await app2.join_chat(invitelink)
            await asyncio.sleep(2)
            await Stenzle.edit_text(
                f"{ASS_NAME} ᴊᴏɪɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ,\n\nsᴛᴀʀᴛɪɴɢ sᴛʀᴇᴀᴍ..."
            )
        except UserAlreadyParticipant:
            pass
        except Exception as ex:
            return await Stenzle.edit_text(
                f"ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴛᴏ {message.chat.title}.\n\n**ʀᴇᴀsᴏɴ :** `{ex}`"
            )
        try:
            await app2.resolve_peer(invitelink)
        except:
            pass

    ruser = message.from_user.first_name
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"» sᴏʀʀʏ ʙᴀʙʏ, ᴛʀᴀᴄᴋ ʟᴏɴɢᴇʀ ᴛʜᴀɴ  {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ᴏɴ {BOT_NAME}."
            )

        file_name = get_file_name(audio)
        title = file_name
        duration = round(audio.duration / 60)
        file_path = (
            await message.reply_to_message.download(file_name)
            if not os.path.isfile(os.path.join("downloads", file_name))
            else f"downloads/{file_name}"
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            title = results[0]["title"]
            duration = results[0]["duration"]
            videoid = results[0]["id"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            return await Stenzle.edit_text(f"sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ\n\n**ᴇʀʀᴏʀ :** `{e}`")

        if (dur / 60) > DURATION_LIMIT:
            return await Stenzle.edit_text(
                f"» sᴏʀʀʏ ʙᴀʙʏ, ᴛʀᴀᴄᴋ ʟᴏɴɢᴇʀ ᴛʜᴀɴ  {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ᴏɴ {BOT_NAME}."
            )
        file_path = audio_dl(url)
    else:
        if len(message.command) < 2:
            return await Stenzle.edit_text("» ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴɴᴀ ᴘʟᴀʏ ʙᴀʙʏ ?")
        query = message.text.split(None, 1)[1]
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            videoid = results[0]["id"]
            duration = results[0]["duration"]

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            LOGGER.error(str(e))
            return await Stenzle.edit("» ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ᴏ̨ᴜᴇʀʏ, ᴛʀʏ ᴘʟᴀʏɪɴɢ ᴀɢᴀɪɴ...")

        if (dur / 60) > DURATION_LIMIT:
            return await Stenzle.edit(
                f"» sᴏʀʀʏ ʙᴀʙʏ, ᴛʀᴀᴄᴋ ʟᴏɴɢᴇʀ ᴛʜᴀɴ  {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ᴏɴ {BOT_NAME}."
            )
        file_path = audio_dl(url)

    try:
        videoid = videoid
    except:
        videoid = "fuckitstgaudio"
        
    if await is_active_chat(message.chat.id):
        await put(
            message.chat.id,
            title,
            duration,
            videoid,
            file_path,
            ruser,
            message.from_user.id,
        )
    else:
        stream = MediaStream(file_path, audio_quality=AudioQuality.STUDIO)
        try:
            await pytgcalls.join_group_call(
                message.chat.id,
                stream,
            )
        except NoActiveGroupCall:
            return await Stenzle.edit_text(
                "**» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ ғᴏᴜɴᴅ.**\n\nᴩʟᴇᴀsᴇ ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ."
            )
        # Note: UnMuteNeeded block is removed as it's no longer a distinct importable exception
        
        await stream_on(message.chat.id)
        await add_active_chat(message.chat.id)
        
    return await Stenzle.delete()
