import os
import datetime
from selenium import webdriver
from send_schedule import send_todayschedule, get_schedule
from justbefore_race import get_justbefore_race
from get_odds import get_odds
from keiba import keiba
from vote import vote

def main():
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )
    driver.get("https://keiba.rakuten.co.jp")
 
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    if datetime.time(9, 00) <= datetime.datetime.now(tz_jst).time() <= datetime.time(9, 30):
        race_list = get_schedule(driver)
        send_todayschedule(race_list)

    else:
        race_list = [['帯広ば', '1R', '13:50', 'はるさん誕生日おめでとう…', 'ダ200m', '9頭'], ['帯広ば', '2R', '14:25', '塩崎翔大君お誕生日記念\u3000…', 'ダ200m', '9頭']]
        if len(race_list) == 0:
            print("今日の全レースは終了しました")
            return False
        justbefore_race, notjustbefore_race = get_justbefore_race(race_list, 10)
        justbefore_race = [['大井', '10R', '20:50', '師走特別競走\u3000Ｃ１一\u3000選…', 'ダ1000m', '12頭']]

        if len(justbefore_race) >= 1:
            race = justbefore_race[0]
            venue, race_R, starting_time, race_name, distance, num_horse = race
            race_R = int(race_R[:-1])
            num_horse = int(num_horse[:-1])
            if num_horse <= 100:
                want_odds = {"単勝"}
                odds = get_odds(driver, venue, race_R, want_odds)
                vote_pattern = keiba(odds)
                vote(driver, vote_pattern)

        race_list = notjustbefore_race
    driver.close()
if __name__ == "__main__":
    main()