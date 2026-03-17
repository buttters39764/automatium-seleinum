import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from automation.config.config import (
    LoginUrl,
    Timeout,
    VisualDelay,
    DefaultLoginUsername,
    DefaultLoginPassword,
)
from automation.logging.logger import info, warning, debug

SUCCESS_SELECTOR = "main-layout"
ERROR_SELECTOR = "vaadin-login-form[error]"


def _perform_login(driver, username: str, password: str):
    info(f"[INFO] Login oldal megnyitása: {LoginUrl}")
    driver.get(LoginUrl)

    wait = WebDriverWait(driver, Timeout)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "vaadin-login-form")))
        info("[INFO] Login form megtalálva.")
    except TimeoutException:
        raise RuntimeError(f"Login form nem jelent meg {Timeout} mp-en belül.")

    info(f"[INFO] Bejelentkezési adatok küldése userrel: {username}")
    actions = ActionChains(driver)
    actions.send_keys(username)
    actions.send_keys(Keys.TAB)
    actions.send_keys(password)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    time.sleep(VisualDelay)
    debug(f"[DEBUG] Login submit után aktuális URL: {driver.current_url}")


def _wait_login_result(driver, timeout: int = 10) -> bool:
    info(f"[INFO] Login eredményre várakozás ({timeout} mp)...")
    end_time = time.time() + timeout

    while time.time() < end_time:
        if driver.find_elements(By.CSS_SELECTOR, SUCCESS_SELECTOR):
            info("[INFO] Siker selector észlelve (main-layout).")
            return True

        if driver.find_elements(By.CSS_SELECTOR, ERROR_SELECTOR):
            warning("[WARN] Hiba selector észlelve (vaadin-login-form[error]).")
            return False

        if "/login" not in driver.current_url.lower():
            info(f"[INFO] URL fallback szerint sikeres login: {driver.current_url}")
            return True

        time.sleep(0.3)

    warning(f"[WARN] Login result wait timeout. Aktuális URL: {driver.current_url}")
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
        info(f"[INFO] Default user login indul: {DefaultLoginUsername}")
        _perform_login(driver, DefaultLoginUsername, DefaultLoginPassword)

        if _wait_login_result(driver):
            info("[OK] Sikeres bejelentkezés (default).")
            return

        raise RuntimeError("Default user login sikertelen.")

    attempts = 0
    while attempts < max_attempts:
        username = input("Felhasználónév: ").strip()
        password = input("Jelszó: ").strip()

        _perform_login(driver, username, password)

        if _wait_login_result(driver):
            info("[OK] Sikeres bejelentkezés.")
            return

        attempts += 1
        warning(f"[WARN] Sikertelen bejelentkezés. ({attempts}/{max_attempts})")

    raise RuntimeError("Túl sok sikertelen bejelentkezési próbálkozás.")