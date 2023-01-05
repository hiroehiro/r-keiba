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
    race_list_url = "../data/race_list.txt"
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    if datetime.time(3, 45) <= datetime.datetime.now(tz_jst).time() <= datetime.time(3, 55):
        driver.get("https://keiba.rakuten.co.jp")
        race_list = get_schedule(driver)
        send_todayschedule(race_list)
        with open(race_list_url, "w") as f:
            f.write(str(race_list))

    else:
        with open(race_list_url, "r") as f:
            race_list = eval(f.read())

        if len(race_list) == 0:
            print("今日の全レースは終了しました")
            driver.close() 
            return False

        justbefore_race, notjustbefore_race = get_justbefore_race(race_list, 10)
        if len(justbefore_race) >= 1:
            for race in justbefore_race:
                venue, race_R, starting_time, race_name, distance, num_horse = race
                race_R = int(race_R[:-1])
                num_horse = int(num_horse[:-1])
                want_odds = {"単勝", "馬単"}
                odds = get_odds(driver, venue, race_R, want_odds)
                ans, cancel_horse_list = keiba(odds)
                print("------------------------------------")
                print(len(ans))
                print(ans)
                print(cancel_horse_list)
                print("------------------------------------")

                    # vote_pattern = keiba(odds)
                    # vote(driver, vote_pattern)
        race_list = notjustbefore_race


        with open(race_list_url, "w") as f:
            f.write(str(notjustbefore_race))


def main():
    schedule.every(5).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()