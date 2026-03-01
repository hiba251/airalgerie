from __future__ import annotations
from dataclasses import dataclass
from typing import List
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@dataclass
class ScrapeConfig:
    url: str
    headless: bool = True
    timeout: int = 25
    delay: float = 1.5
    max_items: int = 200


class AirAlgerieOffersScraper:
    def __init__(self, config: ScrapeConfig):
        self.config = config
        self.driver = None

    def _build_driver(self):
        options = Options()
        if self.config.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1400,900")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def __enter__(self):
        self._build_driver()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.driver:
            self.driver.quit()

    def extract_raw_texts(self) -> List[str]:
        assert self.driver is not None
        self.driver.get(self.config.url)

        WebDriverWait(self.driver, self.config.timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(self.config.delay)

        texts: List[str] = []
        seen = set()

        for _ in range(4):
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a, div, span, p")
            for el in elements:
                try:
                    t = (el.get_attribute("innerText") or "").strip()
                except Exception:
                    continue

                if not t:
                    continue

                if ("From" in t) or ("DZD" in t) or ("EUR" in t) or ("USD" in t) or ("CAD" in t):
                    t = " ".join(t.split())
                    if t not in seen:
                        seen.add(t)
                        texts.append(t)

                if len(texts) >= self.config.max_items:
                    return texts

            time.sleep(0.6)

        return texts