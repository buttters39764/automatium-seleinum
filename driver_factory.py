from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from config import DEFAULT_BROWSER


def _start_firefox():
    options = FirefoxOptions()
    return webdriver.Firefox(options=options)


def _start_chrome():
    options = ChromeOptions()
    return webdriver.Chrome(options=options)


def _start_edge():
    options = EdgeOptions()
    return webdriver.Edge(options=options)


def create_driver():
    starters = {
        "firefox": _start_firefox,
        "chrome": _start_chrome,
        "edge": _start_edge,
    }

    default_browser = (DEFAULT_BROWSER or "firefox").strip().lower()
    if default_browser not in starters:
        default_browser = "firefox"

    # Windows fallback sorrend:
    # 1) config default
    # 2) a maradék fix sorrendben: firefox -> chrome -> edge
    ordered = [default_browser] + [b for b in ["firefox", "chrome", "edge"] if b != default_browser]

    last_error = None
    for browser in ordered:
        try:
            driver = starters[browser]()
            driver.maximize_window()
            print(f"[INFO] Böngésző indul: {browser}")
            return driver
        except WebDriverException as e:
            print(f"[WARN] {browser} nem indult: {e.__class__.__name__}")
            last_error = e

    raise RuntimeError(
        "Nem sikerült böngészőt indítani. Ellenőrizd, hogy Firefox/Chrome/Edge közül legalább egy telepítve van."
    ) from last_error