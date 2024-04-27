import os
import time
import datetime
from selenium import webdriver
import schedule
from schedule_app import get_todayschedule
from get_payout import get_payout
from get_odds import get_odds
import pytz
import pickle
import pandas as pd
from config import full_gate, venue_id

def job():
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )
    japan_timezone = pytz.timezone('Asia/Tokyo')
    
    with open(f"all_racetime.pkl", "rb") as f:
        all_racetime = pickle.load(f)

    for venue, racetime_dict in all_racetime.items():
        for race_time in racetime_dict.keys():
            now = datetime.datetime.now(japan_timezone)
            race_time_datetime = now.replace(hour=int(race_time.split(":")[0]), minute=int(race_time.split(":")[1]), second=0, microsecond=0)

            if race_time_datetime < now:
                continue

            one_hour_later = now + datetime.timedelta(hours=1)
            ff_min_later = now + datetime.timedelta(minutes=55)
            
            race_R = racetime_dict[race_time][0]
            if ff_min_later <= race_time_datetime <= one_hour_later and len(racetime_dict[race_time]) == 1:
                odds = get_odds(driver, venue, race_R)
                racetime_dict[race_time].extend(odds)
                

            thirty_min_later = now + datetime.timedelta(minutes=30)
            tf_min_later = now + datetime.timedelta(minutes=25)
            if tf_min_later <= race_time_datetime <= thirty_min_later and len(racetime_dict[race_time]) == 1 + 3*full_gate:
                odds = get_odds(driver, venue, race_R)
                racetime_dict[race_time].extend(odds)
            
            ten_min_later = now + datetime.timedelta(minutes=10)
            five_min_later = now + datetime.timedelta(minutes=5)
            if five_min_later < race_time_datetime < ten_min_later and len(racetime_dict[race_time]) == 1 + 3*full_gate*2:
                odds = get_odds(driver, venue, race_R)
                racetime_dict[race_time].extend(odds)

    with open(f"all_racetime.pkl", "wb") as f:
        pickle.dump(all_racetime, f)


def dump_today_schedule():
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )

    all_racetime = get_todayschedule(driver)
    with open(f"all_racetime.pkl", "wb") as f:
        pickle.dump(all_racetime, f)

def add_database():
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )

    with open(f"all_racetime.pkl", "rb") as f:
        all_racetime = pickle.load(f)

    df = pd.read_csv("../data/odds_result.csv")

    for venue, racetime_dict in all_racetime.items():
        now_venue_id = venue_id[venue]
        race_r_list, payout_list = get_payout(driver, venue)

        for time, odds in racetime_dict.items():
            R = odds[0]
            payout = payout_list[race_r_list.index(f"■{R}R")]

            if len(odds) == 1:
                continue
            odds = [now_venue_id] + [None if i is None or i == '-' else float(i) for i in odds[1:]] + [payout]
            
            try:
                odds_df = pd.DataFrame([odds], columns=df.columns)
            except ValueError:
                continue
            df = pd.concat([df, odds_df], ignore_index=True)


    df.to_csv("../data/odds_result.csv", index=False)

def main():
    # 当日のレーススケジュールを取得
    schedule.every().day.at("23:00").do(dump_today_schedule)
    schedule.every(5).minutes.do(job)

    # 本日のレーススケジュール結果を保存
    schedule.every().day.at("14:00").do(add_database)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # dump_today_schedule()
    # job()
    # main()
    add_database()