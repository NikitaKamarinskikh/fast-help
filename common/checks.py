import re
from datetime import datetime


def is_correct_date(string: str) -> bool:
    if re.match(r"^\d\d\.\d\d\.\d\d\d\d$", string):
        current_year = datetime.now().year
        days, months, years = string.split(".")
        if int(days) in range(1, 32) and int(months) in range(1, 13) \
                and int(years) in range(current_year, current_year + 2):
            return True
    return False


def is_correct_time(string: str) -> bool:
    if re.match(r"^\d{1,2}:\d\d$", string):
        hours, minutes = string.split(":")
        if int(hours) in range(0, 25) and int(minutes) in range(0, 61):
            return True
    elif re.match(r"^\d{1,2}-\d\d$", string):
        hours, minutes = string.split("-")
        if int(hours) in range(0, 25) and int(minutes) in range(0, 61):
            return True
    return False


def parse_date(string: str):
    """
    date format: dd.mm.yyyy hh:mm
    """
    if re.match(r"^\d\d\.\d\d\.\d\d\d\d \d{1,2}:\d\d$", string):
        date, time = string.split(" ")
        if is_correct_date(date) and is_correct_time(time):
            return datetime.strptime(f"{date} {time}", "%d.%m.%Y %H:%M")
    return None
