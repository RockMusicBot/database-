# Powered By 😁🤭🌝🥰🤡❤️😎❣️🔥🌚😍🤩😏🤗

import asyncio
from traceback import format_exc
from pyrogram.errors import RPCError

from ShrutixMusic import app
from config import LOG_GROUP_ID  # Logger group ID

async def notify_logger_about_crash(error: Exception):
    error_text = (
        "🚨 <b><u>Bot Crash Alert</u></b>\n\n"
        f"<b>Error:</b> <code>{str(error)}</code>\n\n"
        f"<b>Traceback:</b>\n<pre>{format_exc()}</pre>"
    )
    try:
        await app.send_message(
            chat_id=LOG_GROUP_ID,
            text=error_text,
            disable_web_page_preview=True
        )
    except RPCError:
        pass

def logger_alert_on_crash(func):
    async def wrapper(client, *args, **kwargs):
        try:
            return await func(client, *args, **kwargs)
        except Exception as e:
            await notify_logger_about_crash(e)
            raise  # Optional: re-raise for higher-level logging if needed
    return wrapper

def setup_global_exception_handler():
    loop = asyncio.get_event_loop()

    def handle_exception(loop, context):
        error = context.get("exception")
        if error:
            asyncio.create_task(notify_logger_about_crash(error))

    loop.set_exception_handler(handle_exception)
