import datetime
from typing import Tuple
from selenium.webdriver.common.by import By
from utils import stop
from password import *

def get_justbefore_race(race_list: list, minutes_ago: int) -> Tuple[list, list]:
    """
    

    Args:
        race_list (list): _description_

    Returns:
        _type_: _description_
    """
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    
    justbefore_race = []
    notjustbefore_race = []
    for race in race_list:
        race_date = datetime.datetime.strptime(race[2], "%H:%M")
        if (race_date - datetime.timedelta(minutes=minutes_ago)).time() <= datetime.datetime.now(tz_jst).time():
            notjustbefore_race.append(race)
        else:
            justbefore_race.append(race)
    return justbefore_race, notjustbefore_race