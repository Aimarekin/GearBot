from datetime import datetime

from Util import Pages, Utils
from database.DatabaseConnector import Reminder

cache = dict()


def add_reminder(user_id, channel_id, to_remind, end):
    Reminder.create(user_id = user_id, channel_id = channel_id, to_remind = to_remind,
                    start = datetime.now(), end = end, status = "")
    if f"{user_id}" in cache.keys():
        del cache[f"{user_id}"]

async def get_reminder_pages(user_id, must_pending):
    if f"{user_id}" not in cache.keys():
        if must_pending:
            reminders = Reminder.select().where((Reminder.user_id == user_id) & (active == True)).order_by(Reminder.id.desc())
        else:
            reminders = Reminder.select().where(Reminder.user_id == user_id).order_by(Reminder.id.desc())

        out = ""
        longest_pending = 6
        longest_id = len(str(reminders[0].id)) if len(reminders) > 0 else 2
        if not must_pending:
            for reminder in reminders:
                if reminder.active:
                    longest_pending = 5
                    break
        else:
            longest_pending = 7
        for reminder in reminders:
            out += f"{Utils.pad(str(reminder.id), longest_id)} | {Utils.pad(str(reminder.active), longest_active)} | {reminder.start} | {reminder.end} | {reminder.to_remind}\n"
        prefix = f"{Utils.pad('id', longest_id)} | {Utils.pad('active', longest_active)}| start               | end                 | reminder"
        prefix = f"``md`\n{prefix}\n{'-' * len(prefix)}\n"
        pages = Pages.paginate(out, prefix=prefix, suffix="```")
        cache[f"user_id"] = pages
    if len(cache.keys()) > 20:
        del cache[list(cache.keys())[0]]
    return cache[f"{guild_id}_{query}"]
