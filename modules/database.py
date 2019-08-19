from pony.orm import Database, Required, IntArray, Optional, StrArray

db = Database("sqlite", "../F1-bot.db", create_db=True)


class User(db.Entity):
    chatId = Required(int)
    status = Required(str, default="normal")
    wantsNotifications = Required(bool, default=True)
    notificationsHour = Required(str, default="13:30")


class Race(db.Entity):
    number = Required(int)
    state = Required(str)
    date = Required(IntArray)
    disputed = Required(bool, default=False)
    n01 = Optional(StrArray)
    n02 = Optional(StrArray)
    n03 = Optional(StrArray)
    n04 = Optional(StrArray)
    n05 = Optional(StrArray)
    n06 = Optional(StrArray)
    n07 = Optional(StrArray)
    n08 = Optional(StrArray)
    n09 = Optional(StrArray)
    n10 = Optional(StrArray)
    n11 = Optional(StrArray)
    n12 = Optional(StrArray)
    n13 = Optional(StrArray)
    n14 = Optional(StrArray)
    n15 = Optional(StrArray)
    n16 = Optional(StrArray)
    n17 = Optional(StrArray)
    n18 = Optional(StrArray)
    n19 = Optional(StrArray)
    n20 = Optional(StrArray)


db.generate_mapping(create_tables=True)
