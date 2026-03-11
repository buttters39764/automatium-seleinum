from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from login import login_interactive


def main():
    options = Options()
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()

    try:
        login_interactive(driver)
        input("Nyomj Entert a bezáráshoz... ")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()