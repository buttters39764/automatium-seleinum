import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


LOGIN_URL = "https://kokirteszt.kozlekedes.gov.hu/login"


def run_login():
    username = os.getenv("KOKIRT_USERNAME")
    password = os.getenv("KOKIRT_PASSWORD")

    if not username or not password:
        raise ValueError(
            "Hiányzó belépési adatok. Állítsd be: KOKIRT_USERNAME és KOKIRT_PASSWORD"
        )

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get(LOGIN_URL)

    # Adjunk kis időt, hogy betöltődjön az oldal
    time.sleep(2)

    # TODO: ellenőrizd az input mezők pontos azonosítóit (id/name) DevTools-szal
    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")

    user_input.clear()
    user_input.send_keys(username)

    pass_input.clear()
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.ENTER)

    # Várunk kicsit a navigációra
    time.sleep(3)

    print("Login submit megtörtént. Ellenőrizd, hogy sikeres volt-e a belépés.")
    # driver.quit()  # ha kész vagy a teszttel, vedd vissza


if __name__ == "__main__":
    run_login()