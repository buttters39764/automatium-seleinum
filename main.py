from automation.config.config import (
    EXIT_DOT_DELAY_SECONDS,
    EXIT_DOT_COUNT,
    CLEAR_CONSOLE_ON_MAIN_MENU_SHOW,
)
from automation.driver.driver_factory import create_driver
from automation.auth.login import login_interactive
from automation.menu.menu_prompt import ask_user_action
from automation.ui.ui import animated_exit, clear_console


def main():
    driver = create_driver()
    try:
        login_interactive(driver)

        while True:
            if CLEAR_CONSOLE_ON_MAIN_MENU_SHOW:
                clear_console()

            action = ask_user_action()
            if action is None:
                animated_exit(EXIT_DOT_DELAY_SECONDS, EXIT_DOT_COUNT)
                break

            result = action.run(driver)
            if result.message:
                print(f"[OK] {result.message}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()