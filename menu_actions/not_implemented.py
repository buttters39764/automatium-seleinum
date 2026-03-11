from config import EXIT_DOT_DELAY_SECONDS, EXIT_DOT_COUNT
from ui import animated_exit
from menu_actions.base import MenuAction, ActionResult


class NotImplementedAction(MenuAction):
    def __init__(self, key: str, label: str):
        self.key = key
        self.label = label

    def run(self, driver):
        print(f"{self.label}: fejlesztés alatt.")
        print("q) Kilépés")

        while True:
            choice = input("Választás: ").strip().lower()
            if choice == "q":
                animated_exit(EXIT_DOT_DELAY_SECONDS, EXIT_DOT_COUNT)
                return ActionResult(True, "Visszalépés a főmenübe.")
            print("Érvénytelen választás, próbáld újra.")