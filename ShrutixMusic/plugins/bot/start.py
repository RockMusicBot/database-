import time
import asyncio
from typing import Final

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch

import config
from ShrutixMusic import nand
from ShrutixMusic.misc import _boot_
from ShrutixMusic.plugins.sudo.sudoers import sudoers_list
from ShrutixMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ShrutixMusic.utils import bot_sys_stats
from ShrutixMusic.utils.decorators.language import LanguageStart
from ShrutixMusic.utils.formatters import get_readable_time
from ShrutixMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


async def get_user_photo(user_id, user_first_name=None):
    try:
        user_photos = []
        async for photo in nand.get_chat_photos(user_id, limit=1):
            user_photos.append(photo)
        
        if user_photos:
            return user_photos[0].file_id
        else:
            return config.START_IMG_URL
    except Exception as e:
        print(f"Error getting user photo for {user_id}: {e}")
        return config.START_IMG_URL


@nand.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    user_photo = await get_user_photo(message.from_user.id, message.from_user.first_name)

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = help_pannel(_)
            await message.reply_photo(
                photo=user_photo,
                caption=_["help_1"].format(config.SUPPORT_GROUP),
                reply_markup=keyboard,
            )

        elif name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await nand.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} just started sudo check.\n"
                         f"User ID: <code>{message.from_user.id}</code>\n"
                         f"Username: @{message.from_user.username}",
                )
            return

        elif name.startswith("inf"):
            m = await message.reply_text("🔎")
            query = name.replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched = _["start_6"].format(
                title, duration, views, published, channellink, channel, nand.mention
            )
            key = InlineKeyboardMarkup([
                [InlineKeyboardButton(text=_["S_B_8"], url=link),
                 InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_GROUP)],
            ])
            await m.delete()
            await message.reply_photo(
                photo=thumbnail,
                caption=searched,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await nand.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} requested track info.\n"
                         f"User ID: <code>{message.from_user.id}</code>\n"
                         f"Username: @{message.from_user.username}",
                )

    else:
        out = private_panel(_)
        UP, CPU, RAM, DISK = await bot_sys_stats()

        await message.reply_photo(
            photo=user_photo,
            caption=_["start_2"].format(
                message.from_user.mention, nand.mention, UP, DISK, CPU, RAM
            ),
            reply_markup=InlineKeyboardMarkup(out)
        )
                
        if await is_on_off(2):
            return await nand.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} just started the bot.\n"
                     f"User ID: <code>{message.from_user.id}</code>\n"
                     f"Username: @{message.from_user.username}",
            )


@nand.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    user_photo = await get_user_photo(message.from_user.id, message.from_user.first_name)

    out = start_panel(_)
    uptime = int(time.time() - _boot_)

    await message.reply_photo(
        photo=user_photo,
        caption=_["start_1"].format(nand.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out)
    )

    await add_served_chat(message.chat.id)


@nand.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == nand.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await nand.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            nand.mention,
                            f"https://t.me/{nand.username}?start=sudolist",
                            config.SUPPORT_GROUP,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await nand.leave_chat(message.chat.id)

                out = start_panel(_)
                
                user_photo = await get_user_photo(message.from_user.id, message.from_user.first_name)
                
                await message.reply_photo(
                    photo=user_photo,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        nand.mention,
                        message.chat.title,
                        nand.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                        
                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)
            


