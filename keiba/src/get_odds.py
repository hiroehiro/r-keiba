from datetime import datetime
import selenium
from selenium.webdriver.common.by import By
from utils import wait

def get_odds(driver, venue : str, race_R: int, want_oddstype: set) -> dict:
    """
    対象レースのオッズを取得する
    馬複，ワイド，三連複，三連単は未実装

    Args:
        driver
        venue (str): 開催レース場
        race_R (int): 第何Rか
        want_oddstype (set): オッズが欲しい馬券の種類

    Returns:
        dict: want_oddstypeにあるオッズ
    """
    venue_dict = {"帯広ば": "0300000000", "門別": "3600000000", "盛岡": "1000000000", "水沢": "1100000000",
                  "浦和": "1800000000", "船橋": "1900000000", "大井": "2000000000", "川崎": "2100000000",
                  "金沢": "2200000000", "笠松": "2300000000", "名古屋": "2400000000", "園田": "2700000000",
                  "姫路": "2800000000", "高知": "3100000000", "佐賀": "3200000000"}
    
    today = datetime.now().strftime("%Y%m%d")
    driver.get(f"https://keiba.rakuten.co.jp/race_card/list/RACEID/{today}{venue_dict[venue]}")
    wait(1)
    driver.find_element(By.CLASS_NAME, f"race{race_R:02}").find_element(By.PARTIAL_LINK_TEXT, "オッズ").click()
    wait(1)
    
    odds = {}
    if "単勝" in want_oddstype:
        odds["単勝"] = get_odds_WinPlace(driver, "oddsWin")
    if "複勝" in want_oddstype:
        odds["複勝"] = get_odds_WinPlace(driver, "oddsPlace")
    if "枠複" in want_oddstype:
        odds["枠複"] = get_odds_waku(driver, "枠複")
    if "枠単" in want_oddstype:
        odds["枠単"] = get_odds_waku(driver, "枠単")
    # if "馬複" in want_oddstype:
    #     odds["馬複"] = get_odds_waku(driver, "馬複")
    if "馬単" in want_oddstype:
        odds["馬単"] = get_odds_waku(driver, "馬単")
    # if "ワイド" in want_oddstype:
    #     odds["ワイド"] = get_odds_waku(driver, "ワイド")

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