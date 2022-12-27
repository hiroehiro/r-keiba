from selenium.webdriver.common.by import By
from utils import wait, switch_window
from password import *
import os
def vote(driver, vote_pattern: dict):
    original_window = driver.current_window_handle
    driver.find_element(By.PARTIAL_LINK_TEXT, "投票する").click()
    switch_window(driver, original_window)

    wait()
    driver.find_element(By.NAME, "u").send_keys(user_id)
    driver.find_element(By.NAME, "p").send_keys(r_password)
    wait()
    driver.find_element(By.NAME, "submit").click()
    
    if "単勝" in vote_pattern.keys():
        for i, money in enumerate(vote_pattern["単勝"]):
            if money != 0:
                driver.find_element(By.XPATH, f"//*[@id='umaban_{i+1:02}']/td[5]").click()
                wait(0.1)
                driver.find_element(By.ID, "baseAmount").clear()
                wait(0.5)
                driver.find_element(By.ID, "baseAmount").send_keys(money//100)
                wait(0.1)
                driver.find_element(By.PARTIAL_LINK_TEXT, "セット").click()


        now_money = int(driver.find_element(By.XPATH, "//*[@id='menuBar']/div/div[2]/div/ul/li[2]/span[2]").text)
        vote_money = sum(vote_pattern["単勝"])
        
        if now_money < vote_money:
            payment(driver, vote_money-now_money)

        driver.find_element(By.PARTIAL_LINK_TEXT, "投票内容を確認する").click()
        wait()
        driver.find_element(By.XPATH, "//*[@id='confirmForm']/div/table/tbody/tr/td/input[2]").send_keys(sum(vote_pattern["単勝"]))
        wait(1)
        driver.find_element(By.PARTIAL_LINK_TEXT, "投票する").click()
        wait()

        width = driver.execute_script("return document.body.scrollWidth;")
        height = driver.execute_script("return document.body.scrollHeight;")
        driver.set_window_size(width,height)

        #スクショをPNG形式で保存
        driver.get_screenshot_as_file(os.getcwd() + str(i) + ".png")


def payment(driver, add_money: int) -> None:
    """
    入金処理を行う

    Args:
        driver
        add_money (int): 入金する金額
    """
    driver.find_element(By.PARTIAL_LINK_TEXT, "入金").click()
    wait()
    driver.find_element(By.XPATH, "//*[@id='dialogDepositingInputPrice']").send_keys(add_money)
    driver.find_element(By.XPATH, "//*[@id='mainInform01']").click()
    wait()
    driver.find_element(By.PARTIAL_LINK_TEXT, "確認").click()
    wait()
    driver.find_element(By.XPATH, "//*[@id='dialogDepositingConfirmPin']").send_keys(PIN)
    wait(1)
    driver.find_element(By.PARTIAL_LINK_TEXT, "入金する").click()
    wait()
    driver.find_element(By.PARTIAL_LINK_TEXT, "閉じる").click()
    wait()