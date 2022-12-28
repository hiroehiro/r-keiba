import os
import time
import datetime
from selenium import webdriver
import schedule
from send_schedule import send_todayschedule, get_schedule
from justbefore_race import get_justbefore_race
from get_odds import get_odds
from keiba import keiba
from vote import vote

def job():
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )
    driver.get("https://keiba.rakuten.co.jp")

    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    if datetime.time(13, 50) <= datetime.datetime.now(tz_jst).time() <= datetime.time(14, 5):
        race_list = get_schedule(driver)
        send_todayschedule(race_list)
        with open("data/race_list.txt", "w") as f:
            f.write(race_list)

    else:
        with open("data/race_list.txt", "r") as f:
            race_list = eval(f.read())

        if len(race_list) == 0:
            print("今日の全レースは終了しました")
            return False
        justbefore_race, notjustbefore_race = get_justbefore_race(race_list, 10)
        print(justbefore_race)
        # if len(justbefore_race) >= 1:
        #     race = justbefore_race[0]
        #     venue, race_R, starting_time, race_name, distance, num_horse = race
        #     race_R = int(race_R[:-1])
        #     num_horse = int(num_horse[:-1])
        #     if num_horse <= 100:
        #         want_odds = {"単勝"}
        #         odds = get_odds(driver, venue, race_R, want_odds)
        #         vote_pattern = keiba(odds)
        #         vote(driver, vote_pattern)

    driver.close()

    with open("data/race_list.txt", "w") as f:
        f.write(str(notjustbefore_race))


def main():
    schedule.every(5).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()