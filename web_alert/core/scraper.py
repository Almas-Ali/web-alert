"""Web scraper module for fetching and parsing web content."""

import logging
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class WebScraper:
    """Handles web page fetching and content extraction."""

    def __init__(self, timeout: int = 10):
        """
        Initialize the web scraper.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def fetch_content(self, url: str, selector: Optional[str] = None) -> Optional[str]:
        """
        Fetch content from a URL.

        Args:
            url: The URL to fetch
            selector: Optional CSS selector to extract specific content

        Returns:
            The fetched content or None if error occurs
        """
        try:
            logger.info(f"Fetching content from: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            if selector:
                return self._extract_by_selector(response.text, selector)
            else:
                return response.text

        except requests.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

    def _extract_by_selector(self, html: str, selector: str) -> Optional[str]:
        """
        Extract content using CSS selector.

        Args:
            html: HTML content
            selector: CSS selector

        Returns:
            Extracted content or None
        """
        try:
            soup = BeautifulSoup(html, "lxml")
            elements = soup.select(selector)

            if elements:
                # Combine all matching elements
                content = "\n".join([elem.get_text(strip=True) for elem in elements])
                logger.info(
                    f"Extracted {len(elements)} elements using selector '{selector}'"
                )
                return content
            else:
                logger.warning(f"No elements found for selector '{selector}'")
                return None

        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return None

    def get_page_title(self, url: str) -> Optional[str]:
        """
        Get the page title from URL.

        Args:
            url: The URL to fetch

        Returns:
            Page title or None
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            soup = BeautifulSoup(response.text, "lxml")
            title = soup.find("title")
            return title.get_text(strip=True) if title else None
        except Exception as e:
            logger.error(f"Error getting page title: {e}")
            return None

    def close(self):
        """Close the session."""
        self.session.close()
