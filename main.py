from automation.config.config import (
    ExitDotDelaySeconds,
    ExitDotCount,
    ClearConsoleOnMainMenuShow,
)
from automation.driver.driver_factory import create_driver
from automation.auth.login import login_interactive
from automation.menu.menu_prompt import ask_user_action
from automation.ui.ui import animated_exit, clear_console
from automation.logging.logger import setup_logging, info, warning, exception


def main():
    setup_logging()
    info("[INFO] Program indul.")

    driver = create_driver()
    try:
        login_interactive(driver)

        while True:
            if ClearConsoleOnMainMenuShow:
                clear_console()

            action = ask_user_action()
            if action is None:
                animated_exit(ExitDotDelaySeconds, ExitDotCount)
                break

            result = action.run(driver)
            if result.message:
                info(f"[OK] {result.message}")

    except KeyboardInterrupt:
        warning("[WARN] Futtatás megszakítva felhasználó által (Ctrl+C).")
    except Exception as e:
        exception(f"[HIBA] Váratlan hiba a main ciklusban: {e}")
        raise
    finally:
        driver.quit()
        info("[INFO] Driver leállítva.")


if __name__ == "__main__":
    main()