from pony.orm import Database, Required, Optional, IntArray

db = Database("sqlite", "../F1-bot.db", create_db=True)


class User(db.Entity):
    chatId = Required(int)
    status = Required(str, default="normal")


class Race(db.Entity):
    state = Required(str)


class Data(db.Entity):
    general = Required(bool)
    disputedRaces = Optional(IntArray)


db.generate_mapping(create_tables=True)
