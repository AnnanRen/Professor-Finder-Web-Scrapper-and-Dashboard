"""
CloakBrowser integration for bypassing anti-bot detection.
Falls back to stealth Chromium when regular HTTP requests are blocked.
"""
import logging
from bs4 import BeautifulSoup
from typing import Optional

logger = logging.getLogger(__name__)

_cloak_available = False
try:
    from cloakbrowser import launch as cloak_launch
    _cloak_available = True
except ImportError:
    logger.warning("CloakBrowser not installed. Install with: pip install cloakbrowser")


class CloakFetcher:
    """Uses CloakBrowser's stealth Chromium to fetch pages that block regular requests."""

    def __init__(self, headless: bool = True, humanize: bool = True):
        self.headless = headless
        self.humanize = humanize
        self._browser = None
        self.enabled = _cloak_available
        if not self.enabled:
            logger.warning("CloakFetcher disabled: cloakbrowser not available")

    def _ensure_browser(self):
        if self._browser is None and self.enabled:
            self._browser = cloak_launch(headless=self.headless, humanize=self.humanize)

    def fetch(self, url: str, timeout: int = 30) -> Optional[BeautifulSoup]:
        """Fetch a page using CloakBrowser and return BeautifulSoup."""
        if not self.enabled:
            return None
        try:
            self._ensure_browser()
            page = self._browser.new_page()
            page.goto(url, timeout=timeout * 1000)
            html = page.content()
            page.close()
            return BeautifulSoup(html, "lxml")
        except Exception as e:
            logger.warning(f"CloakBrowser fetch failed for {url}: {e}")
            return None

    def close(self):
        if self._browser:
            self._browser.close()
            self._browser = None
