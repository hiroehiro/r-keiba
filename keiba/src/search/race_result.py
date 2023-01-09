from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By

import time

driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )

for year in range(2019, 2024):
    for month in range(1, 13):
        for day in range(1, 32):
            print(f"{year}{month:02}{day:02}")
            time.sleep(1)
            race_result_list = []
            driver.get(f"https://keiba.rakuten.co.jp/race_dividend/list/RACEID/{year}{month:02}{day:02}0000000000")
            time.sleep(0.5)
            venue_list = ["帯広ば", "門　別", "盛　岡", "水　沢", "浦　和", "船　橋", "大　井", 
            "川　崎", "金　沢", "笠　松", "名古屋", "園　田", "姫　路", "高　知" "佐　賀"]
            for venue in venue_list:
                try:
                    driver.find_element(By.PARTIAL_LINK_TEXT, venue).click()
                    time.sleep(1)
                    race_name_list = driver.find_element(By.CLASS_NAME, "contentsList").find_elements(By.CLASS_NAME, "headline")
                    race_name_list = [i.text for i in race_name_list]
                except selenium.common.exceptions.NoSuchElementException:
                    continue

                race_list = []

                for j in range(len(race_name_list)):
                    race_table = driver.find_elements(By.CLASS_NAME, "contentsTable")
                    b = driver.find_elements(By.PARTIAL_LINK_TEXT, "競走成績")

                    trs = race_table[j].find_elements(By.TAG_NAME, "tr")
                    tansyou = trs[0]
                    hukusyou = trs[1]
                    tansyou_win = tansyou.find_element(By.CLASS_NAME, "number").text.split()
                    hukusyou_wins = hukusyou.find_element(By.CLASS_NAME, "number").text.split()
                    b[j+1].click()
                    time.sleep(1)
                    driver.find_element(By.PARTIAL_LINK_TEXT, "オッズ").click()

                    odds = []
                    for i in range(1, 20):
                        try:
                            box_list = driver.find_elements(By.CLASS_NAME, f"box{i:02}")
                            for box in box_list:
                                odds.append(box.find_element(By.CLASS_NAME, "oddsWin").text)
                        except selenium.common.exceptions.NoSuchElementException:
                            continue
                    race_list.append([race_name_list[j], tansyou_win, hukusyou_wins, odds])
                    try:
                        driver.back()
                        time.sleep(1)
                        driver.back()
                        time.sleep(1)
                    except selenium.common.exceptions.WebDriverException:
                        continue
                
                with open("../../data/race_result.txt", "a") as f:
                    f.write(str([f"{year}{month:02}{day:02}", venue, race_list])+"\n")


driver.close()