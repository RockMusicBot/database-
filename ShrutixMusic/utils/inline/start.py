from pyrogram.types import InlineKeyboardButton

import config
from ShrutixMusic import nand


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{nand.username}?startgroup=true",
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],
                url=config.SUPPORT_CHAT,
            ),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                callback_data="settings_back_helper",
            ),
            InlineKeyboardButton(
                text=_["L_N_G"],
                callback_data="LG"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{nand.username}?startgroup=true",
            ),
        ],
    ]
    return buttons
