import os
import datetime
from selenium import webdriver
from send_schedule import send_todayschedule, get_schedule
from justbefore_race import get_justbefore_race, get_oddz
from keiba import keiba

def main():
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )
 
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    if datetime.time(9, 00) <= datetime.datetime.now(tz_jst).time() <= datetime.time(9, 10):
        race_list = get_schedule(driver)
        send_todayschedule(race_list)

    else:
        race_list = [['帯広ば', '1R', '13:50', 'はるさん誕生日おめでとう…', 'ダ200m', '9頭'], ['帯広ば', '2R', '14:25', '塩崎翔大君お誕生日記念\u3000…', 'ダ200m', '9頭']]
        if len(race_list) == 0:
            print("今日の全レースは終了しました")
            return False
        
        justbefore_race, notjustbefore_race = get_justbefore_race(race_list, 10)
        print(justbefore_race)
        print("-----------------------------")
        print(notjustbefore_race)

    #     print(justbefore_race)
    #     if len(justbefore_race) >= 1:
    #         race = justbefore_race[0]
    #         venue, _, _, _, num_horse = race
    #         num_horse = int(num_horse[:-1])
    #         if num_horse <= 9:
    #             print(race)
    #             oddz = get_oddz(driver, venue)
    #             print(oddz)
    #             ans = keiba(oddz)
    #             print(ans)
    #             if len(ans) >= 1:
    #                 subject = '有効レース'
    #                 message = create_message(subject, ans)
    #                 send(message)

    #     upload_gcpstorage(str(notjustbefore_race))
    driver.close()
if __name__ == "__main__":
    main()