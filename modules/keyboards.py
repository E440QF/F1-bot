from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def start(msg_id):
    return InlineKeyboardMarkup(inline_keyboard=
            [[
                InlineKeyboardButton(text="🏎 Latest Race", callback_data="latest#{}".format(msg_id)),
                InlineKeyboardButton(text="➡️ Next", callback_data="next#{}".format(msg_id))
                ], [
                InlineKeyboardButton(text="⏮ Previous Races", callback_data="previous#{}".format(msg_id))
                ], [
                InlineKeyboardButton(text="⏭ Upcoming Races", callback_data="upcoming#{}".format(msg_id))
                ]
            ])


def back(msg_id):
    return InlineKeyboardMarkup(inline_keyboard=
            [
                [InlineKeyboardButton(text="◀️ Main Menu", callback_data="start#{}".format(msg_id))]
            ])
