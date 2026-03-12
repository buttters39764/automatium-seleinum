from dataclasses import dataclass
from selenium.webdriver.remote.webdriver import WebDriver


@dataclass
class ActionResult:
    ok: bool
    message: str = ""


class MenuAction:
    key: str = ""
    label: str = ""

    def run(self, driver: WebDriver) -> ActionResult:
        raise NotImplementedError