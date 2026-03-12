from automation.config.config import (
    EXIT_DOT_DELAY_SECONDS,
    EXIT_DOT_COUNT,
    CLEAR_CONSOLE_ON_SUBMENU_ENTER,
    CLEAR_CONSOLE_ON_SUBMENU_EXIT,
)
from automation.ui.ui import animated_exit, clear_console
from automation.actions.base import MenuAction, ActionResult


class NotImplementedAction(MenuAction):
    def __init__(self, key: str, label: str):
        self.key = key
        self.label = label

    def run(self, driver):
        if CLEAR_CONSOLE_ON_SUBMENU_ENTER:
            clear_console()

        print(f"{self.label}: fejlesztés alatt.")
        print("q) Kilépés")

        while True:
            choice = input("Választás: ").strip().lower()
            if choice == "q":
                animated_exit(EXIT_DOT_DELAY_SECONDS, EXIT_DOT_COUNT)
                if CLEAR_CONSOLE_ON_SUBMENU_EXIT:
                    clear_console()
                return ActionResult(True, "Visszalépés a főmenübe.")
            print("Érvénytelen választás, próbáld újra.")