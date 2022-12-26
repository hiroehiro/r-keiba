import selenium
from selenium.webdriver.common.by import By
from utils import stop, create_message, send

def get_schedule(driver) -> list:
    """
    楽天競馬トップページから
    本日の開催競馬場と開催レース情報を取得する

    Args:
        driver

    Returns:
        list: 本日の開催情報
    """
    racecourse_list = [i.text for i in driver.find_elements(By.CLASS_NAME, "name") if i.text != ""]
    race_list = []
    for course in racecourse_list:
        driver.find_element(By.PARTIAL_LINK_TEXT, course).click()
        stop()
        for i in range(1, 20):
            try:
                race_info = driver.find_element(By.CLASS_NAME, f"race{i:02}").text.split("\n")[0].split(" ")
            except selenium.common.exceptions.NoSuchElementException:
                break
            
            race_list.append([course]+race_info[:5])
        driver.back()
    return race_list

def send_todayschedule(race_list: list) -> None:
    """
    本日の開催情報をメールで送信する

    Args:
        race_list (list): 開催情報
    """
    todayschedule = str(race_list)
    subject = '今日の競馬日程'
    message = create_message(subject, todayschedule)
    send(message)