from pony.orm import Database, Required  # , Optional, StrArray

db = Database("sqlite", "../F1-bot.db", create_db=True)


class User(db.Entity):
    chatId = Required(int)
    status = Required(str, default="normal")
    wantsNotifications = Required(bool, default=True)
    notificationsHour = Required(str, default="13:30")


class Race(db.Entity):
    state = Required(str)


db.generate_mapping(create_tables=True)
