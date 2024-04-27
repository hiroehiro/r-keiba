import datetime
import pytz
import selenium
from selenium.webdriver.common.by import By
from utils import wait, create_message, send
from config import venue_dict

def get_todayschedule(driver) -> list:
    """
    楽天競馬トップページから
    本日の開催競馬場と開催レース時間を取得する

    Args:
        driver
        today (str): 今日の日付 %Y%m%d

    Returns:
        list: 本日の開催情報
    """
    japan_timezone = pytz.timezone('Asia/Tokyo')
    today = datetime.datetime.now(japan_timezone).strftime("%Y%m%d")
    schedule_url = f"https://keiba.rakuten.co.jp/odds/tanfuku/RACEID/{today}"

    all_racetime = {}
    for venue, id in venue_dict.items():
        driver.get(schedule_url+id)
        wait()
        
        racenumber_list = [i.text for i in driver.find_elements(By.CLASS_NAME, "raceNumber") if i.text]
    
        if len(racenumber_list) == 0:
            all_racetime[venue] = {}
            continue

        assert len(racenumber_list) ==1, "レース数の形式が変わりました"
        assert racenumber_list[0].split("\n")[3] == "1R", "レース数の形式が変わりました"

        racenumber_list = racenumber_list[0].split("\n")[3:]

        racetime_list = []
        for i in range(0, len(racenumber_list), 2):
            try:
                racetime_list.append(racenumber_list[i+1])
            except IndexError:
                break

        all_racetime[venue] = {time: [r+1] for r, time in enumerate(racetime_list)}
    return all_racetime

def send_todayschedule(race_list: list) -> None:
    """
    本日の開催情報をメールで送信する

    Args:
        race_list (list): 開催情報
    """
    todayschedule = str(race_list)
    subject = '今日の競馬日程'
    message = create_message(subject, todayschedule)
    send(message)


if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )
    print(get_todayschedule(driver))