import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import LOGGER_ID
from ShrutixMusic import nand
from ShrutixMusic.utils.database import add_served_chat, get_assistant, delete_served_chat

@nand.on_message(filters.new_chat_members, group=-10)
async def join_watcher(_, message):
    try:
        userbot = await get_assistant(message.chat.id)
        for member in message.new_chat_members:
            if member.id == nand.id:
                count = await nand.get_chat_members_count(message.chat.id)
                username = message.chat.username if message.chat.username else "Private Group"

                invite_link = ""
                try:
                    if not message.chat.username:
                        link = await nand.export_chat_invite_link(message.chat.id)
                        invite_link = f"\n🔗 Group Link: {link}" if link else ""
                except:
                    pass

                caption = (
                    f"🎵 <b>Music Bot Added!</b>\n\n"
                    f"📝 <b>Chat Name:</b> {message.chat.title}\n"
                    f"🆔 <b>Chat ID:</b> {message.chat.id}\n"
                    f"👥 <b>Members:</b> {count}\n"
                    f"🙋 <b>Added By:</b> {message.from_user.mention}"
                    f"{invite_link}\n\n"
                    f"#Added"
                )

                buttons = [
                    [InlineKeyboardButton("🙋 Added By", url=f"tg://openmessage?user_id={message.from_user.id}")]
                ]

                await nand.send_message(
                    LOGGER_ID,
                    text=caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )

                await add_served_chat(message.chat.id)
                if username:
                    await userbot.join_chat(f"@{username}")

    except Exception as e:
        print(f"Error: {e}")

@nand.on_message(filters.left_chat_member, group=-12)
async def on_left_chat_member(_, message):
    try:
        userbot = await get_assistant(message.chat.id)
        left_member = message.left_chat_member

        if left_member and left_member.id == (await nand.get_me()).id:
            removed_by = message.from_user.mention if message.from_user else "Unknown User"

            caption = (
                f"❌ <b>Music Bot Left Group!</b>\n\n"
                f"📝 <b>Chat Name:</b> {message.chat.title}\n"
                f"🆔 <b>Chat ID:</b> {message.chat.id}\n"
                f"🙋 <b>Removed By:</b> {removed_by}\n\n"
                f"#Left"
            )

            await nand.send_message(LOGGER_ID, text=caption)
            await delete_served_chat(message.chat.id)
            await userbot.leave_chat(message.chat.id)

    except Exception:
        return
