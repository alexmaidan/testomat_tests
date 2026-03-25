from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ProjectCard:

    def __init__(self, element: WebElement):
        self._element = element

    @property
    def title(self) -> str:
        return self._element.find_element(By.TAG_NAME, "h3").text

    @property
    def tests_count_text(self) -> str:
        return self._element.find_element(By.CSS_SELECTOR, "p.text-gray-500").text

    @property
    def badge(self) -> str:
        return self._element.find_element(By.CSS_SELECTOR, ".project-badges .common-badge").text

    @property
    def href(self) -> str:
        return self._element.find_element(By.TAG_NAME, "a").get_attribute("href")

    def is_visible(self) -> bool:
        return self._element.is_displayed()

    def get_member_avatars_count(self) -> int:
        return len(self._element.find_elements(By.CSS_SELECTOR, ".inline-flex img"))

    def click(self) -> None:
        self._element.find_element(By.TAG_NAME, "a").click()