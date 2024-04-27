import datetime
import selenium
from selenium.webdriver.common.by import By
from utils import wait
from config import venue_dict, full_gate
import pytz


def get_payout(driver, venue: str):
    """
    対象レースの払い戻しを取得する

    Args:
        driver
        venue (str): 開催レース場
    """

    japan_timezone = pytz.timezone('Asia/Tokyo')
    today = datetime.datetime.now(japan_timezone).strftime("%Y%m%d")

    driver.get(f"https://keiba.rakuten.co.jp/race_dividend/list/RACEID/{today}{venue_dict[venue]}")
    wait(2)

    race_r_list = [i.text for i in driver.find_elements(By.CLASS_NAME, "headline") if i.text][1:-1]
    race_r_list = [i.split(' ')[0] for i in race_r_list]
    race_r_check = [i[0] for i in race_r_list if i[0] == '■' and i[-1] == 'R']
    assert len(race_r_list) == len(race_r_check), "レース数の形式が変わりました"

    payout_list = [i.text for i in driver.find_elements(By.CLASS_NAME, "contentsTable") if i.text][:-1]
    payout_list_check = [i[0] for i in payout_list if i[:2] == '単勝']
    assert len(payout_list) == len(payout_list_check), "払い戻しの形式が変わりました"
    
    assert len(payout_list) == len(race_r_list), 'レース数と払い戻し数が一致しません'

    payout_list = [int(i.split(' ')[2].replace(',', '')) for i in payout_list]

    return race_r_list, payout_list

if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )
    get_payout(driver, "佐賀")
    driver.quit()