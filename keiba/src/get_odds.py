import datetime
import selenium
from selenium.webdriver.common.by import By
from utils import wait
from config import venue_dict, full_gate
import pytz

def get_odds(driver, venue : str, race_R: int) -> dict:
    """
    対象レースの単勝複勝オッズを取得する

    Args:
        driver
        venue (str): 開催レース場
        race_R (int): 第何Rか
        today (str): 今日の日付 %Y%m%d

    Returns:
        list, list: 単勝オッズ，複勝オッズ
    """
    japan_timezone = pytz.timezone('Asia/Tokyo')
    today = datetime.datetime.now(japan_timezone).strftime("%Y%m%d")
    
    driver.get(f"https://keiba.rakuten.co.jp/odds/tanfuku/RACEID/{today}{venue_dict[venue][:-2]}{race_R:02}")
    oddsWin_list = [i.text for i in driver.find_elements(By.CLASS_NAME, "oddsWin") if i.text]
    oddsPlace_list = [i.text for i in driver.find_elements(By.CLASS_NAME, "oddsPlace") if i.text]
    
    assert len(oddsWin_list) > 1, "オッズの形式が変わりました"
    assert len(oddsPlace_list) > 1, "オッズの形式が変わりました"
    assert oddsWin_list[0] == "単勝\nオッズ", "オッズの形式が変わりました"
    assert oddsPlace_list[0] == "複勝\nオッズ", "オッズの形式が変わりました"
    assert len(oddsWin_list) == len(oddsPlace_list), "オッズの形式が変わりました"

    oddsWin_list = oddsWin_list[1:]
    oddsPlace_list = oddsPlace_list[1:]

    oddsPlace_list = [n for item in oddsPlace_list for n in item.split(" - ")]
    
    # フルゲートまで埋める
    oddsWin_list.extend([None] * (full_gate-len(oddsWin_list)))
    oddsPlace_list.extend([None] * (2*full_gate-len(oddsPlace_list)))

    assert len(oddsWin_list) == full_gate, "オッズの数が足りません"
    assert len(oddsPlace_list) == 2*full_gate, "オッズの数が足りません"

    odds = oddsWin_list + oddsPlace_list

    wait(1)

    return odds


def get_odds_WinPlace(driver, oddstype: str) -> list:
    """
    単勝，複勝のオッズを取得する

    Args:
        driver 
        oddstype (str): 単勝or複勝

    Returns:
        list: オッズ
    """
    odds = []
    for i in range(1, 20):
        try:
            box_list = driver.find_elements(By.CLASS_NAME, f"box{i:02}")
            for box in box_list:
                odds.append(box.find_element(By.CLASS_NAME, oddstype).text)
        except selenium.common.exceptions.NoSuchElementException:
            continue
    return odds

def get_odds_waku(driver, oddstype: str) -> list:
    """
    枠複，枠単，馬単のオッズを取得する

    Args:
        driver 
        oddstype (str):枠複or枠単or馬単 

    Returns:
        list: オッズ
    """
    odds = []
    driver.find_element(By.PARTIAL_LINK_TEXT, oddstype).click()
    wait()
    for j in range(1, 4):
        for i in range(1, 20):
            try:
                t = driver.find_element(By.XPATH, f"//*[@id='wakuUmaBanJun']/table[{j}]/tbody/tr[{i}]")
                if j == 1:
                    odds.append([float(tt.text) if tt.text != "-" else tt.text for tt in t.find_elements(By.TAG_NAME, "td")])
                else:
                    odds[i-1].extend([float(tt.text) if tt.text != "-" else tt.text for tt in t.find_elements(By.TAG_NAME, "td")])
            
            except (selenium.common.exceptions.NoSuchElementException, IndexError):
                continue

    odds = [list(x) for x in zip(*odds)] #転置
    driver.back()
    return odds


if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )
    get_odds(driver, "帯広ば", 2)