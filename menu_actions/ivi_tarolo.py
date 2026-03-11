from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import (
    EXIT_DOT_DELAY_SECONDS,
    EXIT_DOT_COUNT,
    CLEAR_CONSOLE_ON_SUBMENU_ENTER,
    CLEAR_CONSOLE_ON_SUBMENU_EXIT,
)
from ui import animated_exit, clear_console
from menu_actions.base import MenuAction, ActionResult


class IVITaroloAction(MenuAction):
    key = "1"
    label = "IVI tároló"

    def run(self, driver):
        if CLEAR_CONSOLE_ON_SUBMENU_ENTER:
            clear_console()

        while True:
            print("\nIVI tároló menü")
            print("1) új IVI")
            print("q) Kilépés")

            sub = input("Választás: ").strip().lower()

            if sub == "1":
                wait = WebDriverWait(driver, 20)
                if "/ivi-lister" not in driver.current_url.lower():
                    driver.get("http://d01.np:9004/ivi-lister")

                wait.until(EC.url_contains("/ivi-lister"))
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ivi-lister")))
                print("[OK] IVI tároló oldal megnyitva.")
                continue

            if sub == "q":
                animated_exit(EXIT_DOT_DELAY_SECONDS, EXIT_DOT_COUNT)
                if CLEAR_CONSOLE_ON_SUBMENU_EXIT:
                    clear_console()
                return ActionResult(True, "Visszalépés a főmenübe.")

            print("Érvénytelen választás, próbáld újra.")