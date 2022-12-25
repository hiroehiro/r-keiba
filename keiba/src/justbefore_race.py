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
            justbefore_race.append(race)
        else:
            notjustbefore_race.append(race)
    return justbefore_race, notjustbefore_race

def get_oddz(driver, venue):
    w_list = ['月', '火', '水', '木', '金', '土', '日']
    driver.get('https://n.ipat.jra.go.jp/sp/index.cgi')
    driver.find_element(By.ID,"userid").send_keys(userid)
    driver.find_element(By.ID,"password").send_keys(userpassward)
    driver.find_element(By.ID,"pars").send_keys(pars)
    stop()
    driver.find_element(By.CLASS_NAME, 'btnBrown').click()
    stop()
    driver.find_element(By.CLASS_NAME, 'ico_ods').click()
    stop()
    course_list = driver.find_element(By.CLASS_NAME, 'selectList').find_elements(By.CLASS_NAME, "ui-link")
    stop()
    driver.find_element(By.PARTIAL_LINK_TEXT, f"{venue}({w_list[datetime.date.today().weekday()]})").click()
    stop()
    race_list = driver.find_element(By.CLASS_NAME, 'selectList').find_elements(By.CLASS_NAME, "ui-link")
    driver.find_element(By.PARTIAL_LINK_TEXT, race_list[0].text).click()
    stop()
    driver.find_element(By.PARTIAL_LINK_TEXT, "式別から選択").click()
    stop()
    driver.find_element(By.PARTIAL_LINK_TEXT, "馬単").click()
    stop()
    driver.find_element(By.PARTIAL_LINK_TEXT, "ＯＫ").click()
    stop(0.5)
    driver.find_element(By.PARTIAL_LINK_TEXT, "1着ながし").click()
    stop()
    horse_list = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul').text.split("\n")[3:]
    oddz = []
    horsename_list = []
    for i in range(len(horse_list)//3):
        try:
            horsename_list.append(horse_list[3*i + 1])
            oddz.append([horse_list[3*i + 2]])
        except:
            oddz.append([None])
    stop()

    for i in range(len(horsename_list)):
        driver.find_element(By.PARTIAL_LINK_TEXT, horsename_list[i]).click()
        stop(0.8)
        driver.find_element(By.PARTIAL_LINK_TEXT, "全選択").click()
        stop()
        driver.find_element(By.PARTIAL_LINK_TEXT, "オッズ選択画面へ").click()
        stop()
        exacta = driver.find_element(By.XPATH, '/html/body/div[1]/div/ul').text.split("\n")
        stop()
        oddz[i] += exacta[2::3]
        driver.find_element(By.PARTIAL_LINK_TEXT, "式別選択画面へ").click()
        stop()
        driver.find_element(By.PARTIAL_LINK_TEXT, "馬単").click()
        t(0.5)
        driver.find_element(By.PARTIAL_LINK_TEXT, "ＯＫ").click()
        stop()
        driver.find_element(By.PARTIAL_LINK_TEXT, "1着ながし").click()
        stop()

    oddz = [i for i in oddz if i != [None]]
    return oddz