from automation.config.config import (
    ExitDotDelaySeconds,
    ExitDotCount,
    ClearConsoleOnSubmenuEnter,
    ClearConsoleOnSubmenuExit,
)
from automation.ui.ui import animated_exit, clear_console
from automation.actions.base import MenuAction, ActionResult


class NotImplementedAction(MenuAction):
    def __init__(self, key: str, label: str):
        self.key = key
        self.label = label

    def run(self, driver):
        if ClearConsoleOnSubmenuEnter:
            clear_console()

        print(f"{self.label}: fejlesztés alatt.")
        print("q) Kilépés")

        while True:
            choice = input("Választás: ").strip().lower()
            if choice == "q":
                animated_exit(ExitDotDelaySeconds, ExitDotCount)
                if ClearConsoleOnSubmenuExit:
                    clear_console()
                return ActionResult(True, "Visszalépés a főmenübe.")
            print("Érvénytelen választás, próbáld újra.")