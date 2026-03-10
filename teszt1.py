import os
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "http://d01.np:9004/login"


def run_login():
    username = os.getenv("KOKIRT_USERNAME")
    password = os.getenv("KOKIRT_PASSWORD")
    if not username or not password:
        raise ValueError("Hiányzó belépési adatok. Állítsd be: KOKIRT_USERNAME és KOKIRT_PASSWORD")

    options = Options()
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)

    driver.get(LOGIN_URL)

    # Várjuk meg, hogy maga a login komponens ott legyen
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-login-form")))

    # Emberi tab-olás: user -> pass -> enter
    actions = ActionChains(driver)
    actions.send_keys(username)
    actions.send_keys(Keys.TAB)
    actions.send_keys(password)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    # kis várakozás, hogy lásd mi történik
    time.sleep(5)

    print("URL login után:", driver.current_url)
    input("Nyomj Entert a bezáráshoz... ")
    driver.quit()


if __name__ == "__main__":
    run_login()