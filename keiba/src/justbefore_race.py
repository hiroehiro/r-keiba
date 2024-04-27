import datetime
from typing import Tuple
from selenium.webdriver.common.by import By
from utils import wait
from password import *

def get_justbefore_race(race_list: list, minutes_ago: int) -> Tuple[list, list]:
    """
    開始直前のレースとそうでないレースに分割する

    Args:
        race_list (list): 開催レースの情報


    Returns:
        _type_: _description_
    """
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))    
    justbefore_race = []
    notjustbefore_race = []
    for race in race_list:
        race_date = datetime.datetime.strptime(race[2], "%H:%M")
        if (race_date - datetime.timedelta(minutes=minutes_ago)).time() <= datetime.datetime.now(tz_jst).time():
            justbefore_race.append(race)
        else:
            notjustbefore_race.append(race)
    return justbefore_race, notjustbefore_race

def get_before_race(race_list: list, minutes_ago: int) -> Tuple[list, list]:
    """
    開始前のレースを得る

    Args:
        race_list (list): 開催レースの情報


    Returns:
        _type_: _description_
    """
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))    
    now = datetime.datetime.now(tz_jst)

    time_ago = datetime.datetime.strptime(f"{now.hour}:{now.minute}", "%H:%M") - datetime.timedelta(minutes=minutes_ago)
    time_ago = datetime.datetime.strptime(f"{time_ago.hour}:{time_ago.minute}", "%H:%M")
    time_ago = datetime.datetime(now.year, now.month, now.day, time_ago.hour, time_ago.minute)


    justbefore_race = []
    print(time_ago, race_list)
    for race in race_list:
        race_date = datetime.datetime.strptime(race[2], "%H:%M")
        if abs((race_date - time_ago).total_seconds()) <= 120:
            justbefore_race.append(race)

    return justbefore_race