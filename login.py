import os
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import LOGIN_URL, TIMEOUT, VISUAL_DELAY


SUCCESS_SELECTOR = "main-layout"
ERROR_SELECTOR = "vaadin-login-form[error]"
LOGIN_OVERLAY_OPEN_SELECTOR = "vaadin-login-overlay-wrapper[opened]"


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
    """
    True => sikeres login
    False => sikertelen login
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        # siker: main-layout megjelenik
        if driver.find_elements(By.CSS_SELECTOR, SUCCESS_SELECTOR):
            return True

        # hiba: vaadin-login-form error állapotban
        if driver.find_elements(By.CSS_SELECTOR, ERROR_SELECTOR):
            return False

        # URL alapú fallback
        if "/login" not in driver.current_url.lower():
            return True

        time.sleep(0.3)

    # timeout fallback
    return "/login" not in driver.current_url.lower()


def login_interactive(driver, max_attempts: int = 5):
    default_user = os.getenv("DEFAULT_KOKIRT_USERNAME", "")
    default_pass = os.getenv("DEFAULT_KOKIRT_PASSWORD", "")
    default_pin = os.getenv("DEFAULT_LOGIN_PIN", "")

    while True:
        mode = input("Bejelentkezés default userrel? (i/n): ").strip().lower()
        if mode in ("i", "n"):
            break
        print("Érvénytelen választás. i vagy n")

    if mode == "i":
        if not (default_user and default_pass and default_pin):
            raise ValueError("Hiányzik DEFAULT_LOGIN_PIN vagy default user/pass env változó.")
        while True:
            pin = input("PIN: ").strip()
            if pin == default_pin:
                _perform_login(driver, default_user, default_pass)
                if _wait_login_result(driver):
                    print("Sikeres bejelentkezés (default).")
                    print("URL login után:", driver.current_url)
                    return
                print("Default user login sikertelen. Próbáld újra.")
            else:
                print("Hibás PIN, próbáld újra.")

    attempts = 0
    while attempts < max_attempts:
        username = input("Felhasználónév: ").strip()
        password = input("Jelszó: ").strip()
        _perform_login(driver, username, password)

        if _wait_login_result(driver):
            print("Sikeres bejelentkezés.")
            print("URL login után:", driver.current_url)
            return

        print("Sikertelen bejelentkezés, próbáld újra.")
        attempts += 1

    raise RuntimeError("Túl sok sikertelen bejelentkezési próbálkozás.")