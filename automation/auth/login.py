import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.config.config import (
    LOGIN_URL,
    TIMEOUT,
    VISUAL_DELAY,
    DEFAULT_LOGIN_USERNAME,
    DEFAULT_LOGIN_PASSWORD,
)

SUCCESS_SELECTOR = "main-layout"
ERROR_SELECTOR = "vaadin-login-form[error]"


def _perform_login(driver, username: str, password: str):
    wait = WebDriverWait(driver, TIMEOUT)
    driver.get(LOGIN_URL)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-login-form")))

    actions = ActionChains(driver)
    actions.send_keys(username)
    actions.send_keys(Keys.TAB)
    actions.send_keys(password)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(VISUAL_DELAY)


def _wait_login_result(driver, timeout: int = 10) -> bool:
    end_time = time.time() + timeout
    while time.time() < end_time:
        if driver.find_elements(By.CSS_SELECTOR, SUCCESS_SELECTOR):
            return True
        if driver.find_elements(By.CSS_SELECTOR, ERROR_SELECTOR):
            return False
        if "/login" not in driver.current_url.lower():
            return True
        time.sleep(0.3)
    return "/login" not in driver.current_url.lower()


def login_interactive(driver, max_attempts: int = 5):
    print("Info: Belépés előtt ellenőrizd, hogy az ip címed megfelelő telephelyen legyen a sikeres belépés érdekében.")
    print("Default userrel akarsz belépni?")
    print("Enter = igen / n = nem")

    while True:
        mode = input("Választás (Enter/n): ").strip().lower()
        if mode in ("", "n"):
            break
        print("Érvénytelen választás. Enter vagy n")

    if mode == "":
        print(f"Default user login indul: {DEFAULT_LOGIN_USERNAME}")
        _perform_login(driver, DEFAULT_LOGIN_USERNAME, DEFAULT_LOGIN_PASSWORD)
        if _wait_login_result(driver):
            print("Sikeres bejelentkezés (default).")
            return
        raise RuntimeError("Default user login sikertelen.")

    attempts = 0
    while attempts < max_attempts:
        username = input("Felhasználónév: ").strip()
        password = input("Jelszó: ").strip()
        _perform_login(driver, username, password)

        if _wait_login_result(driver):
            print("Sikeres bejelentkezés.")
            return

        attempts += 1
        print(f"Sikertelen bejelentkezés, próbáld újra. ({attempts}/{max_attempts})")

    raise RuntimeError("Túl sok sikertelen bejelentkezési próbálkozás.")