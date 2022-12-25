from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

if __name__ == '__main__':

    # Selenium サーバへ接続
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions()
    )
    print("aaaaaaaaaaaaaaaaaaa")

    driver.implicitly_wait(10) #seconds
    # 当ブログサイトにアクセス
    driver.get("https://tech-lab.sios.jp/")

    # 検索ボックスに docker と入力して検索
    driver.find_element(By.NAME, "s").send_keys("docker" + Keys.RETURN)

    # 検索結果取得
    result_elems = driver.find_elements(By.CLASS_NAME, "entry-title.mh-posts-list-title")

    # 検索結果よりタイトルを出力
    for elem in result_elems:
        print(elem.text)

    # 検索結果の画面キャプチャを取得し保存
    FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img1.png") #ファイル名
    w = driver.execute_script("return document.body.scrollWidth;")
    h = driver.execute_script("return document.body.scrollHeight;")
    driver.set_window_size(w,h)
    driver.save_screenshot(FILENAME)

    driver.quit()
