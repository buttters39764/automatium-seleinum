from driver_factory import create_driver
from login import login_interactive


def main():
    driver = create_driver()
    try:
        login_interactive(driver)
        input("Nyomj Entert a bezáráshoz... ")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()