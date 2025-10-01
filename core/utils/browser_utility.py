"""
Browser Utility Module using Playwright
Provides comprehensive browser automation utilities for Playwright
Supports multiple browsers, waits, actions, and common web operations
"""

from playwright.sync_api import (
    sync_playwright, Page, Browser, BrowserContext, Locator,
    expect, Error, TimeoutError as PlaywrightTimeoutError
)
from playwright.sync_api import Playwright
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Tuple
import logging
import time
from datetime import datetime
import json
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BrowserUtility:
    """
    Utility class for browser automation using Playwright
    Provides methods for browser initialization, element interactions, and common actions
    """

    def __init__(self):
        """Initialize Browser Utility"""
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.default_timeout = 10000  # Playwright uses milliseconds
        self.screenshot_dir = Path(__file__).parent.parent.parent.parent.parent.parent / "screenshots"
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.downloads_dir = Path(__file__).parent.parent.parent.parent.parent.parent / "downloads"
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        logger.info("BrowserUtility initialized")

    # ==================== Browser Initialization ====================
    def initialize_browser(self, browser_type: str = 'chromium', **kwargs):
        """Initialize browser by type"""
        if not self.playwright:
            self.init_playwright()
        return self.init_browser(browser_type, **kwargs)

    def create_browser_context(self, **options):
        """Create new browser context"""
        if not self.browser:
            raise Exception("Browser not initialized. Call initialize_browser() first")

        if not options:
            options = {
                'viewport': {'width': 1920, 'height': 1080},
                'accept_downloads': True
            }

        self.context = self.browser.new_context(**options)
        return self.context

    def create_page(self):
        """Create new page in current context"""
        if not self.context:
            raise Exception("Context not created. Call create_browser_context() first")

        self.page = self.context.new_page()
        self.page.set_default_timeout(self.default_timeout)
        return self.page


    def init_playwright(self) -> Playwright:
        """
        Initialize Playwright

        Returns:
            Playwright instance
        """
        try:
            self.playwright = sync_playwright().start()
            logger.info("Playwright initialized successfully")
            return self.playwright
        except Exception as e:
            logger.error(f"Error initializing Playwright: {str(e)}")
            raise

    def init_chromium(self, headless: bool = False, slow_mo: int = 0,
                      args: List[str] = None, viewport: Dict = None) -> Browser:
        """
        Initialize Chromium browser

        Args:
            headless: Run in headless mode
            slow_mo: Slow down operations by specified milliseconds
            args: Browser launch arguments
            viewport: Viewport size {'width': 1280, 'height': 720}

        Returns:
            Browser instance
        """
        try:
            if not self.playwright:
                self.init_playwright()

            launch_options = {
                'headless': headless,
                'slow_mo': slow_mo
            }

            if args:
                launch_options['args'] = args

            self.browser = self.playwright.chromium.launch(**launch_options)

            context_options = {
                'viewport': viewport if viewport else {'width': 1920, 'height': 1080},
                'accept_downloads': True,
                'record_video_dir': str(self.screenshot_dir / 'videos') if not headless else None
            }

            self.context = self.browser.new_context(**context_options)
            self.page = self.context.new_page()
            self.page.set_default_timeout(self.default_timeout)

            logger.info("Chromium browser initialized successfully")
            return self.browser

        except Exception as e:
            logger.error(f"Error initializing Chromium browser: {str(e)}")
            raise

    def init_firefox(self, headless: bool = False, slow_mo: int = 0,
                     args: List[str] = None, viewport: Dict = None) -> Browser:
        """
        Initialize Firefox browser

        Args:
            headless: Run in headless mode
            slow_mo: Slow down operations by specified milliseconds
            args: Browser launch arguments
            viewport: Viewport size

        Returns:
            Browser instance
        """
        try:
            if not self.playwright:
                self.init_playwright()

            launch_options = {
                'headless': headless,
                'slow_mo': slow_mo
            }

            if args:
                launch_options['args'] = args

            self.browser = self.playwright.firefox.launch(**launch_options)

            context_options = {
                'viewport': viewport if viewport else {'width': 1920, 'height': 1080},
                'accept_downloads': True
            }

            self.context = self.browser.new_context(**context_options)
            self.page = self.context.new_page()
            self.page.set_default_timeout(self.default_timeout)

            logger.info("Firefox browser initialized successfully")
            return self.browser

        except Exception as e:
            logger.error(f"Error initializing Firefox browser: {str(e)}")
            raise

    def init_webkit(self, headless: bool = False, slow_mo: int = 0,
                    args: List[str] = None, viewport: Dict = None) -> Browser:
        """
        Initialize WebKit browser (Safari)

        Args:
            headless: Run in headless mode
            slow_mo: Slow down operations by specified milliseconds
            args: Browser launch arguments
            viewport: Viewport size

        Returns:
            Browser instance
        """
        try:
            if not self.playwright:
                self.init_playwright()

            launch_options = {
                'headless': headless,
                'slow_mo': slow_mo
            }

            if args:
                launch_options['args'] = args

            self.browser = self.playwright.webkit.launch(**launch_options)

            context_options = {
                'viewport': viewport if viewport else {'width': 1920, 'height': 1080},
                'accept_downloads': True
            }

            self.context = self.browser.new_context(**context_options)
            self.page = self.context.new_page()
            self.page.set_default_timeout(self.default_timeout)

            logger.info("WebKit browser initialized successfully")
            return self.browser

        except Exception as e:
            logger.error(f"Error initializing WebKit browser: {str(e)}")
            raise

    def init_browser(self, browser_name: str = 'chromium', **kwargs) -> Browser:
        """
        Initialize browser by name

        Args:
            browser_name: Browser name ('chromium', 'firefox', 'webkit')
            **kwargs: Additional arguments for browser initialization

        Returns:
            Browser instance
        """
        browser_name = browser_name.lower()

        if browser_name in ['chromium', 'chrome']:
            return self.init_chromium(**kwargs)
        elif browser_name == 'firefox':
            return self.init_firefox(**kwargs)
        elif browser_name in ['webkit', 'safari']:
            return self.init_webkit(**kwargs)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    def close_browser(self) -> None:
        """Close browser and cleanup"""
        try:
            if self.page:
                self.page.close()
                logger.info("Page closed")

            if self.context:
                self.context.close()
                logger.info("Context closed")

            if self.browser:
                self.browser.close()
                logger.info("Browser closed")

            if self.playwright:
                self.playwright.stop()
                logger.info("Playwright stopped")

        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")

    def new_page(self) -> Page:
        """
        Create new page in current context

        Returns:
            Page instance
        """
        try:
            new_page = self.context.new_page()
            new_page.set_default_timeout(self.default_timeout)
            logger.info("New page created")
            return new_page
        except Exception as e:
            logger.error(f"Error creating new page: {str(e)}")
            raise

    def new_context(self, **options) -> BrowserContext:
        """
        Create new browser context

        Args:
            **options: Context options

        Returns:
            BrowserContext instance
        """
        try:
            context = self.browser.new_context(**options)
            logger.info("New context created")
            return context
        except Exception as e:
            logger.error(f"Error creating new context: {str(e)}")
            raise

    # ==================== Navigation Operations ====================

    def navigate_to(self, url: str, wait_until: str = 'domcontentloaded',
                    timeout: int = None) -> None:
        """
        Navigate to URL

        Args:
            url: URL to navigate to
            wait_until: When to consider navigation succeeded
                       ('load', 'domcontentloaded', 'networkidle')
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.goto(url, wait_until=wait_until, timeout=timeout_ms)
            logger.info(f"Navigated to: {url}")
        except Exception as e:
            logger.error(f"Error navigating to {url}: {str(e)}")
            raise

    def reload(self, wait_until: str = 'domcontentloaded', timeout: int = None) -> None:
        """
        Reload current page

        Args:
            wait_until: When to consider reload succeeded
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.reload(wait_until=wait_until, timeout=timeout_ms)
            logger.info("Page reloaded")
        except Exception as e:
            logger.error(f"Error reloading page: {str(e)}")
            raise

    def go_back(self, wait_until: str = 'domcontentloaded', timeout: int = None) -> None:
        """
        Navigate back in history

        Args:
            wait_until: When to consider navigation succeeded
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.go_back(wait_until=wait_until, timeout=timeout_ms)
            logger.info("Navigated back")
        except Exception as e:
            logger.error(f"Error navigating back: {str(e)}")
            raise

    def go_forward(self, wait_until: str = 'domcontentloaded', timeout: int = None) -> None:
        """
        Navigate forward in history

        Args:
            wait_until: When to consider navigation succeeded
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.go_forward(wait_until=wait_until, timeout=timeout_ms)
            logger.info("Navigated forward")
        except Exception as e:
            logger.error(f"Error navigating forward: {str(e)}")
            raise

    def get_url(self) -> str:
        """
        Get current page URL

        Returns:
            Current URL
        """
        try:
            url = self.page.url
            logger.info(f"Current URL: {url}")
            return url
        except Exception as e:
            logger.error(f"Error getting URL: {str(e)}")
            return ""

    def get_title(self) -> str:
        """
        Get current page title

        Returns:
            Page title
        """
        try:
            title = self.page.title()
            logger.info(f"Page title: {title}")
            return title
        except Exception as e:
            logger.error(f"Error getting title: {str(e)}")
            return ""

    # ==================== Element Location ====================

    def locator(self, selector: str) -> Locator:
        """
        Get locator for element

        Args:
            selector: CSS selector, text, or other selector

        Returns:
            Locator instance
        """
        return self.page.locator(selector)

    def get_by_role(self, role: str, **kwargs) -> Locator:
        """
        Get element by ARIA role

        Args:
            role: ARIA role (e.g., 'button', 'link', 'textbox')
            **kwargs: Additional options (name, checked, pressed, etc.)

        Returns:
            Locator instance
        """
        return self.page.get_by_role(role, **kwargs)

    def get_by_text(self, text: str, exact: bool = False) -> Locator:
        """
        Get element by text content

        Args:
            text: Text content to search for
            exact: Match exact text

        Returns:
            Locator instance
        """
        return self.page.get_by_text(text, exact=exact)

    def get_by_label(self, text: str, exact: bool = False) -> Locator:
        """
        Get input element by associated label text

        Args:
            text: Label text
            exact: Match exact text

        Returns:
            Locator instance
        """
        return self.page.get_by_label(text, exact=exact)

    def get_by_placeholder(self, text: str, exact: bool = False) -> Locator:
        """
        Get input element by placeholder

        Args:
            text: Placeholder text
            exact: Match exact text

        Returns:
            Locator instance
        """
        return self.page.get_by_placeholder(text, exact=exact)

    def get_by_test_id(self, test_id: str) -> Locator:
        """
        Get element by test ID

        Args:
            test_id: Test ID attribute value

        Returns:
            Locator instance
        """
        return self.page.get_by_test_id(test_id)

    def get_by_title(self, text: str, exact: bool = False) -> Locator:
        """
        Get element by title attribute

        Args:
            text: Title text
            exact: Match exact text

        Returns:
            Locator instance
        """
        return self.page.get_by_title(text, exact=exact)

    def get_by_alt_text(self, text: str, exact: bool = False) -> Locator:
        """
        Get image by alt text

        Args:
            text: Alt text
            exact: Match exact text

        Returns:
            Locator instance
        """
        return self.page.get_by_alt_text(text, exact=exact)

    def query_selector(self, selector: str) -> Optional[Any]:
        """
        Query single element (returns element handle or None)

        Args:
            selector: CSS selector

        Returns:
            ElementHandle or None
        """
        try:
            element = self.page.query_selector(selector)
            if element:
                logger.info(f"Element found: {selector}")
            else:
                logger.warning(f"Element not found: {selector}")
            return element
        except Exception as e:
            logger.error(f"Error querying selector: {str(e)}")
            return None

    def query_selector_all(self, selector: str) -> List[Any]:
        """
        Query all matching elements

        Args:
            selector: CSS selector

        Returns:
            List of ElementHandles
        """
        try:
            elements = self.page.query_selector_all(selector)
            logger.info(f"Found {len(elements)} elements: {selector}")
            return elements
        except Exception as e:
            logger.error(f"Error querying selectors: {str(e)}")
            return []

    # ==================== Element Interaction ====================

    def click(self, selector: str, timeout: int = None, **kwargs) -> None:
        """
        Click element

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
            **kwargs: Additional options (button, click_count, delay, etc.)
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).click(timeout=timeout_ms, **kwargs)
            logger.info(f"Clicked element: {selector}")
        except Exception as e:
            logger.error(f"Error clicking element: {str(e)}")
            raise

    def double_click(self, selector: str, timeout: int = None, **kwargs) -> None:
        """
        Double click element

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
            **kwargs: Additional options
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).dblclick(timeout=timeout_ms, **kwargs)
            logger.info(f"Double clicked element: {selector}")
        except Exception as e:
            logger.error(f"Error double clicking element: {str(e)}")
            raise

    def right_click(self, selector: str, timeout: int = None, **kwargs) -> None:
        """
        Right click element (context click)

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
            **kwargs: Additional options
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).click(button='right', timeout=timeout_ms, **kwargs)
            logger.info(f"Right clicked element: {selector}")
        except Exception as e:
            logger.error(f"Error right clicking element: {str(e)}")
            raise

    def fill(self, selector: str, text: str, timeout: int = None) -> None:
        """
        Fill input field (clears and types)

        Args:
            selector: Element selector
            text: Text to fill
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).fill(text, timeout=timeout_ms)
            logger.info(f"Filled element: {selector}")
        except Exception as e:
            logger.error(f"Error filling element: {str(e)}")
            raise

    def type(self, selector: str, text: str, delay: int = 0, timeout: int = None) -> None:
        """
        Type text character by character

        Args:
            selector: Element selector
            text: Text to type
            delay: Delay between key presses in milliseconds
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).type(text, delay=delay, timeout=timeout_ms)
            logger.info(f"Typed text in element: {selector}")
        except Exception as e:
            logger.error(f"Error typing in element: {str(e)}")
            raise

    def clear(self, selector: str, timeout: int = None) -> None:
        """
        Clear input field

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).clear(timeout=timeout_ms)
            logger.info(f"Cleared element: {selector}")
        except Exception as e:
            logger.error(f"Error clearing element: {str(e)}")
            raise

    def press(self, selector: str, key: str, timeout: int = None) -> None:
        """
        Press keyboard key on element

        Args:
            selector: Element selector
            key: Key to press (e.g., 'Enter', 'Tab', 'Escape')
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).press(key, timeout=timeout_ms)
            logger.info(f"Pressed key '{key}' on element: {selector}")
        except Exception as e:
            logger.error(f"Error pressing key: {str(e)}")
            raise

    def press_enter(self, selector: str, timeout: int = None) -> None:
        """Press Enter key on element"""
        self.press(selector, 'Enter', timeout)

    def press_tab(self, selector: str, timeout: int = None) -> None:
        """Press Tab key on element"""
        self.press(selector, 'Tab', timeout)

    def press_escape(self, selector: str, timeout: int = None) -> None:
        """Press Escape key on element"""
        self.press(selector, 'Escape', timeout)

    def hover(self, selector: str, timeout: int = None, **kwargs) -> None:
        """
        Hover over element

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
            **kwargs: Additional options
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).hover(timeout=timeout_ms, **kwargs)
            logger.info(f"Hovered over element: {selector}")
        except Exception as e:
            logger.error(f"Error hovering over element: {str(e)}")
            raise

    def focus(self, selector: str, timeout: int = None) -> None:
        """
        Focus on element

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).focus(timeout=timeout_ms)
            logger.info(f"Focused on element: {selector}")
        except Exception as e:
            logger.error(f"Error focusing on element: {str(e)}")
            raise

    def drag_and_drop(self, source_selector: str, target_selector: str,
                      timeout: int = None) -> None:
        """
        Drag and drop element

        Args:
            source_selector: Source element selector
            target_selector: Target element selector
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(source_selector).drag_to(
                self.page.locator(target_selector),
                timeout=timeout_ms
            )
            logger.info(f"Dragged from {source_selector} to {target_selector}")
        except Exception as e:
            logger.error(f"Error in drag and drop: {str(e)}")
            raise

    # ==================== Element Properties ====================

    def get_text(self, selector: str, timeout: int = None) -> str:
        """
        Get element text content

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            Element text
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            text = self.page.locator(selector).text_content(timeout=timeout_ms)
            logger.info(f"Got text from element: {text}")
            return text if text else ""
        except Exception as e:
            logger.error(f"Error getting text: {str(e)}")
            return ""

    def get_inner_text(self, selector: str, timeout: int = None) -> str:
        """
        Get element inner text (rendered text)

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            Element inner text
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            text = self.page.locator(selector).inner_text(timeout=timeout_ms)
            logger.info(f"Got inner text from element: {text}")
            return text
        except Exception as e:
            logger.error(f"Error getting inner text: {str(e)}")
            return ""

    def get_inner_html(self, selector: str, timeout: int = None) -> str:
        """
        Get element inner HTML

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            Element inner HTML
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            html = self.page.locator(selector).inner_html(timeout=timeout_ms)
            logger.info(f"Got inner HTML from element")
            return html
        except Exception as e:
            logger.error(f"Error getting inner HTML: {str(e)}")
            return ""

    def get_attribute(self, selector: str, attribute: str, timeout: int = None) -> Optional[str]:
        """
        Get element attribute value

        Args:
            selector: Element selector
            attribute: Attribute name
            timeout: Custom timeout in milliseconds

        Returns:
            Attribute value or None
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            value = self.page.locator(selector).get_attribute(attribute, timeout=timeout_ms)
            logger.info(f"Got attribute '{attribute}': {value}")
            return value
        except Exception as e:
            logger.error(f"Error getting attribute: {str(e)}")
            return None

    def get_value(self, selector: str, timeout: int = None) -> str:
        """
        Get input element value

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            Input value
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            value = self.page.locator(selector).input_value(timeout=timeout_ms)
            logger.info(f"Got input value: {value}")
            return value
        except Exception as e:
            logger.error(f"Error getting value: {str(e)}")
            return ""

    def is_visible(self, selector: str, timeout: int = None) -> bool:
        """
        Check if element is visible

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            True if visible, False otherwise
        """
        try:
            timeout_ms = timeout if timeout else 1000  # Short timeout for visibility check
            visible = self.page.locator(selector).is_visible(timeout=timeout_ms)
            logger.info(f"Element visible: {visible}")
            return visible
        except:
            return False

    def is_hidden(self, selector: str, timeout: int = None) -> bool:
        """
        Check if element is hidden

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            True if hidden, False otherwise
        """
        try:
            timeout_ms = timeout if timeout else 1000
            hidden = self.page.locator(selector).is_hidden(timeout=timeout_ms)
            logger.info(f"Element hidden: {hidden}")
            return hidden
        except:
            return False

    def is_enabled(self, selector: str, timeout: int = None) -> bool:
        """
        Check if element is enabled

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            True if enabled, False otherwise
        """
        try:
            timeout_ms = timeout if timeout else 1000
            enabled = self.page.locator(selector).is_enabled(timeout=timeout_ms)
            logger.info(f"Element enabled: {enabled}")
            return enabled
        except:
            return False

    def is_disabled(self, selector: str, timeout: int = None) -> bool:
        """
        Check if element is disabled

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            True if disabled, False otherwise
        """
        try:
            timeout_ms = timeout if timeout else 1000
            disabled = self.page.locator(selector).is_disabled(timeout=timeout_ms)
            logger.info(f"Element disabled: {disabled}")
            return disabled
        except:
            return False

    def is_checked(self, selector: str, timeout: int = None) -> bool:
        """
        Check if checkbox/radio is checked

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            True if checked, False otherwise
        """
        try:
            timeout_ms = timeout if timeout else 1000
            checked = self.page.locator(selector).is_checked(timeout=timeout_ms)
            logger.info(f"Element checked: {checked}")
            return checked
        except:
            return False

    def is_editable(self, selector: str, timeout: int = None) -> bool:
        """
        Check if element is editable

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            True if editable, False otherwise
        """
        try:
            timeout_ms = timeout if timeout else 1000
            editable = self.page.locator(selector).is_editable(timeout=timeout_ms)
            logger.info(f"Element editable: {editable}")
            return editable
        except:
            return False

    def count(self, selector: str) -> int:
        """
        Count matching elements

        Args:
            selector: Element selector

        Returns:
            Number of matching elements
        """
        try:
            count = self.page.locator(selector).count()
            logger.info(f"Element count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting elements: {str(e)}")
            return 0

    # ==================== Wait Operations ====================

    def wait_for_selector(self, selector: str, state: str = 'visible',
                          timeout: int = None) -> None:
        """
        Wait for element to reach specific state

        Args:
            selector: Element selector
            state: State to wait for ('attached', 'detached', 'visible', 'hidden')
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.wait_for_selector(selector, state=state, timeout=timeout_ms)
            logger.info(f"Element reached state '{state}': {selector}")
        except PlaywrightTimeoutError:
            logger.error(f"Element did not reach state '{state}' within timeout: {selector}")
            raise

    def wait_for_url(self, url: Union[str, Any], timeout: int = None) -> None:
        """
        Wait for URL to match pattern

        Args:
            url: URL string or regex pattern
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.wait_for_url(url, timeout=timeout_ms)
            logger.info(f"URL matched: {url}")
        except PlaywrightTimeoutError:
            logger.error(f"URL did not match within timeout: {url}")
            raise

    def wait_for_load_state(self, state: str = 'load', timeout: int = None) -> None:
        """
        Wait for page load state

        Args:
            state: Load state ('load', 'domcontentloaded', 'networkidle')
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.wait_for_load_state(state, timeout=timeout_ms)
            logger.info(f"Page reached load state: {state}")
        except PlaywrightTimeoutError:
            logger.error(f"Page did not reach load state '{state}' within timeout")
            raise

    def wait_for_timeout(self, timeout: int) -> None:
        """
        Wait for specified time

        Args:
            timeout: Time to wait in milliseconds
        """
        self.page.wait_for_timeout(timeout)
        logger.info(f"Waited for {timeout}ms")

    def wait_for_function(self, expression: str, timeout: int = None) -> Any:
        """
        Wait for JavaScript function to return truthy value

        Args:
            expression: JavaScript expression
            timeout: Custom timeout in milliseconds

        Returns:
            Result of the expression
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            result = self.page.wait_for_function(expression, timeout=timeout_ms)
            logger.info("JavaScript function returned truthy value")
            return result
        except PlaywrightTimeoutError:
            logger.error("Function did not return truthy value within timeout")
            raise

        # ==================== Dropdown/Select Operations ====================

    def select_option(self, selector: str, value: Union[str, List[str]] = None,
                      label: Union[str, List[str]] = None,
                      index: Union[int, List[int]] = None,
                      timeout: int = None) -> List[str]:
        """
        Select option(s) from dropdown

        Args:
            selector: Select element selector
            value: Option value(s) to select
            label: Option label(s) to select
            index: Option index(es) to select
            timeout: Custom timeout in milliseconds

        Returns:
            List of selected option values
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout

            if value is not None:
                selected = self.page.locator(selector).select_option(
                    value=value, timeout=timeout_ms
                )
            elif label is not None:
                selected = self.page.locator(selector).select_option(
                    label=label, timeout=timeout_ms
                )
            elif index is not None:
                selected = self.page.locator(selector).select_option(
                    index=index, timeout=timeout_ms
                )
            else:
                raise ValueError("Must provide value, label, or index")

            logger.info(f"Selected option(s): {selected}")
            return selected if isinstance(selected, list) else [selected]

        except Exception as e:
            logger.error(f"Error selecting option: {str(e)}")
            raise

    def get_select_options(self, selector: str, timeout: int = None) -> List[Dict[str, str]]:
        """
        Get all options from select element

        Args:
            selector: Select element selector
            timeout: Custom timeout in milliseconds

        Returns:
            List of option dictionaries with 'value' and 'label'
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            options = self.page.locator(f"{selector} option").all()

            option_list = []
            for option in options:
                option_list.append({
                    'value': option.get_attribute('value'),
                    'label': option.inner_text()
                })

            logger.info(f"Got {len(option_list)} options from select")
            return option_list

        except Exception as e:
            logger.error(f"Error getting select options: {str(e)}")
            return []

        # ==================== Checkbox and Radio Operations ====================

    def check(self, selector: str, timeout: int = None) -> None:
        """
        Check checkbox or radio button

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).check(timeout=timeout_ms)
            logger.info(f"Checked element: {selector}")
        except Exception as e:
            logger.error(f"Error checking element: {str(e)}")
            raise

    def uncheck(self, selector: str, timeout: int = None) -> None:
        """
        Uncheck checkbox

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).uncheck(timeout=timeout_ms)
            logger.info(f"Unchecked element: {selector}")
        except Exception as e:
            logger.error(f"Error unchecking element: {str(e)}")
            raise

    def set_checked(self, selector: str, checked: bool, timeout: int = None) -> None:
        """
        Set checkbox state

        Args:
            selector: Element selector
            checked: True to check, False to uncheck
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).set_checked(checked, timeout=timeout_ms)
            logger.info(f"Set checked state to {checked}: {selector}")
        except Exception as e:
            logger.error(f"Error setting checked state: {str(e)}")
            raise

        # ==================== File Upload/Download Operations ====================

    def upload_file(self, selector: str, file_path: Union[str, List[str]],
                    timeout: int = None) -> None:
        """
        Upload file(s)

        Args:
            selector: File input selector
            file_path: Path to file or list of paths for multiple files
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).set_input_files(file_path, timeout=timeout_ms)
            logger.info(f"Uploaded file(s): {file_path}")
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise

    def download_file(self, trigger_selector: str, timeout: int = None) -> str:
        """
        Download file by clicking trigger element

        Args:
            trigger_selector: Selector of element that triggers download
            timeout: Custom timeout in milliseconds

        Returns:
            Path to downloaded file
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout

            with self.page.expect_download(timeout=timeout_ms) as download_info:
                self.page.locator(trigger_selector).click()

            download = download_info.value
            file_path = self.downloads_dir / download.suggested_filename
            download.save_as(file_path)

            logger.info(f"Downloaded file to: {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            raise

        # ==================== Frame Operations ====================

    def switch_to_frame(self, selector: str) -> Any:
        """
        Switch to frame by selector

        Args:
            selector: Frame selector

        Returns:
            Frame object
        """
        try:
            frame = self.page.frame_locator(selector)
            logger.info(f"Switched to frame: {selector}")
            return frame
        except Exception as e:
            logger.error(f"Error switching to frame: {str(e)}")
            raise

    def get_frame_by_name(self, name: str) -> Optional[Any]:
        """
        Get frame by name attribute

        Args:
            name: Frame name

        Returns:
            Frame object or None
        """
        try:
            frame = self.page.frame(name=name)
            if frame:
                logger.info(f"Got frame by name: {name}")
            else:
                logger.warning(f"Frame not found: {name}")
            return frame
        except Exception as e:
            logger.error(f"Error getting frame by name: {str(e)}")
            return None

    def get_frame_by_url(self, url: str) -> Optional[Any]:
        """
        Get frame by URL

        Args:
            url: Frame URL pattern

        Returns:
            Frame object or None
        """
        try:
            frame = self.page.frame(url=url)
            if frame:
                logger.info(f"Got frame by URL: {url}")
            else:
                logger.warning(f"Frame not found for URL: {url}")
            return frame
        except Exception as e:
            logger.error(f"Error getting frame by URL: {str(e)}")
            return None

        # ==================== Alert/Dialog Operations ====================

    def handle_dialog(self, accept: bool = True, prompt_text: str = None) -> None:
        """
        Set up dialog handler

        Args:
            accept: True to accept dialog, False to dismiss
            prompt_text: Text to enter in prompt dialog
        """

        def dialog_handler(dialog):
            logger.info(f"Dialog: {dialog.message}")
            if prompt_text:
                dialog.accept(prompt_text)
            elif accept:
                dialog.accept()
            else:
                dialog.dismiss()

        self.page.on("dialog", dialog_handler)
        logger.info("Dialog handler set up")

    def expect_dialog(self, timeout: int = None):
        """
        Expect and wait for dialog

        Args:
            timeout: Custom timeout in milliseconds

        Returns:
            Dialog context manager
        """
        timeout_ms = timeout if timeout else self.default_timeout
        return self.page.expect_event("dialog", timeout=timeout_ms)

        # ==================== Window/Tab Operations ====================

    def new_tab(self) -> Page:
        """
        Open new tab

        Returns:
            New Page object
        """
        try:
            new_page = self.context.new_page()
            new_page.set_default_timeout(self.default_timeout)
            logger.info("Opened new tab")
            return new_page
        except Exception as e:
            logger.error(f"Error opening new tab: {str(e)}")
            raise

    def switch_to_tab(self, index: int) -> Page:
        """
        Switch to tab by index

        Args:
            index: Tab index (0-based)

        Returns:
            Page object
        """
        try:
            pages = self.context.pages
            if 0 <= index < len(pages):
                self.page = pages[index]
                logger.info(f"Switched to tab {index}")
                return self.page
            else:
                raise IndexError(f"Tab index {index} out of range")
        except Exception as e:
            logger.error(f"Error switching to tab: {str(e)}")
            raise

    def get_all_pages(self) -> List[Page]:
        """
        Get all open pages/tabs

        Returns:
            List of Page objects
        """
        try:
            pages = self.context.pages
            logger.info(f"Got {len(pages)} pages")
            return pages
        except Exception as e:
            logger.error(f"Error getting pages: {str(e)}")
            return []

    def close_tab(self, page: Page = None) -> None:
        """
        Close specific tab

        Args:
            page: Page object to close (default: current page)
        """
        try:
            if page:
                page.close()
            else:
                self.page.close()
            logger.info("Closed tab")
        except Exception as e:
            logger.error(f"Error closing tab: {str(e)}")

        # ==================== Screenshot and Recording ====================

    def take_screenshot(self, file_name: str = None, full_page: bool = False,
                        selector: str = None) -> str:
        """
        Take screenshot

        Args:
            file_name: Screenshot file name (auto-generated if None)
            full_page: Capture full scrollable page
            selector: Capture specific element only

        Returns:
            Path to screenshot file
        """
        try:
            if not file_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"screenshot_{timestamp}.png"

            screenshot_path = self.screenshot_dir / file_name

            if selector:
                self.page.locator(selector).screenshot(path=str(screenshot_path))
            else:
                self.page.screenshot(path=str(screenshot_path), full_page=full_page)

            logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)

        except Exception as e:
            logger.error(f"Error taking screenshot: {str(e)}")
            raise

    def take_screenshot_base64(self, full_page: bool = False) -> str:
        """
        Take screenshot as base64 string

        Args:
            full_page: Capture full scrollable page

        Returns:
            Base64 encoded screenshot
        """
        try:
            screenshot_bytes = self.page.screenshot(full_page=full_page)
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            logger.info("Screenshot captured as base64")
            return screenshot_base64
        except Exception as e:
            logger.error(f"Error taking screenshot: {str(e)}")
            raise

    def start_video_recording(self) -> None:
        """Start video recording (must be enabled in context options)"""
        logger.info("Video recording enabled in context (if configured)")

    def stop_video_recording(self) -> Optional[str]:
        """
        Stop video recording and save

        Returns:
            Path to video file or None
        """
        try:
            if self.page.video:
                video_path = self.page.video.path()
                logger.info(f"Video saved: {video_path}")
                return str(video_path)
            else:
                logger.warning("Video recording not enabled")
                return None
        except Exception as e:
            logger.error(f"Error stopping video recording: {str(e)}")
            return None

        # ==================== JavaScript Execution ====================

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript on page

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to script

        Returns:
            Result of script execution
        """
        try:
            result = self.page.evaluate(script, *args)
            logger.info("JavaScript executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error executing JavaScript: {str(e)}")
            raise

    def execute_script_on_element(self, selector: str, script: str) -> Any:
        """
        Execute JavaScript on specific element

        Args:
            selector: Element selector
            script: JavaScript code (element available as 'element')

        Returns:
            Result of script execution
        """
        try:
            result = self.page.locator(selector).evaluate(script)
            logger.info("JavaScript executed on element")
            return result
        except Exception as e:
            logger.error(f"Error executing JavaScript on element: {str(e)}")
            raise

    def scroll_to_element(self, selector: str, timeout: int = None) -> None:
        """
        Scroll element into view

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        try:
            timeout_ms = timeout if timeout else self.default_timeout
            self.page.locator(selector).scroll_into_view_if_needed(timeout=timeout_ms)
            logger.info(f"Scrolled to element: {selector}")
        except Exception as e:
            logger.error(f"Error scrolling to element: {str(e)}")
            raise

    def scroll_page(self, x: int = 0, y: int = 0) -> None:
        """
        Scroll page by pixels

        Args:
            x: Horizontal scroll pixels
            y: Vertical scroll pixels
        """
        try:
            self.page.evaluate(f"window.scrollBy({x}, {y})")
            logger.info(f"Scrolled page by ({x}, {y})")
        except Exception as e:
            logger.error(f"Error scrolling page: {str(e)}")
            raise

    def scroll_to_top(self) -> None:
        """Scroll to top of page"""
        try:
            self.page.evaluate("window.scrollTo(0, 0)")
            logger.info("Scrolled to top of page")
        except Exception as e:
            logger.error(f"Error scrolling to top: {str(e)}")
            raise

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page"""
        try:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            logger.info("Scrolled to bottom of page")
        except Exception as e:
            logger.error(f"Error scrolling to bottom: {str(e)}")
            raise

        # ==================== Cookie Operations ====================

    def get_cookies(self) -> List[Dict[str, Any]]:
        """
        Get all cookies

        Returns:
            List of cookie dictionaries
        """
        try:
            cookies = self.context.cookies()
            logger.info(f"Got {len(cookies)} cookies")
            return cookies
        except Exception as e:
            logger.error(f"Error getting cookies: {str(e)}")
            return []

    def get_cookie(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get specific cookie by name

        Args:
            name: Cookie name

        Returns:
            Cookie dictionary or None
        """
        try:
            cookies = self.context.cookies()
            for cookie in cookies:
                if cookie['name'] == name:
                    logger.info(f"Got cookie: {name}")
                    return cookie
            logger.warning(f"Cookie not found: {name}")
            return None
        except Exception as e:
            logger.error(f"Error getting cookie: {str(e)}")
            return None

    def add_cookies(self, cookies: List[Dict[str, Any]]) -> None:
        """
        Add cookies to browser context

        Args:
            cookies: List of cookie dictionaries
        """
        try:
            self.context.add_cookies(cookies)
            logger.info(f"Added {len(cookies)} cookies")
        except Exception as e:
            logger.error(f"Error adding cookies: {str(e)}")
            raise

    def clear_cookies(self) -> None:
        """Clear all cookies"""
        try:
            self.context.clear_cookies()
            logger.info("Cleared all cookies")
        except Exception as e:
            logger.error(f"Error clearing cookies: {str(e)}")
            raise

        # ==================== Local/Session Storage ====================

    def get_local_storage(self, key: str) -> Optional[str]:
        """
        Get value from local storage

        Args:
            key: Storage key

        Returns:
            Storage value or None
        """
        try:
            value = self.page.evaluate(f"localStorage.getItem('{key}')")
            logger.info(f"Got local storage value for key: {key}")
            return value
        except Exception as e:
            logger.error(f"Error getting local storage: {str(e)}")
            return None

    def set_local_storage(self, key: str, value: str) -> None:
        """
        Set value in local storage

        Args:
            key: Storage key
            value: Storage value
        """
        try:
            self.page.evaluate(f"localStorage.setItem('{key}', '{value}')")
            logger.info(f"Set local storage: {key}")
        except Exception as e:
            logger.error(f"Error setting local storage: {str(e)}")
            raise

    def clear_local_storage(self) -> None:
        """Clear local storage"""
        try:
            self.page.evaluate("localStorage.clear()")
            logger.info("Cleared local storage")
        except Exception as e:
            logger.error(f"Error clearing local storage: {str(e)}")
            raise

    def get_session_storage(self, key: str) -> Optional[str]:
        """
        Get value from session storage

        Args:
            key: Storage key

        Returns:
            Storage value or None
        """
        try:
            value = self.page.evaluate(f"sessionStorage.getItem('{key}')")
            logger.info(f"Got session storage value for key: {key}")
            return value
        except Exception as e:
            logger.error(f"Error getting session storage: {str(e)}")
            return None

    def set_session_storage(self, key: str, value: str) -> None:
        """
        Set value in session storage

        Args:
            key: Storage key
            value: Storage value
        """
        try:
            self.page.evaluate(f"sessionStorage.setItem('{key}', '{value}')")
            logger.info(f"Set session storage: {key}")
        except Exception as e:
            logger.error(f"Error setting session storage: {str(e)}")
            raise

    def clear_session_storage(self) -> None:
        """Clear session storage"""
        try:
            self.page.evaluate("sessionStorage.clear()")
            logger.info("Cleared session storage")
        except Exception as e:
            logger.error(f"Error clearing session storage: {str(e)}")
            raise

        # ==================== Network Operations ====================

    def set_offline(self, offline: bool = True) -> None:
        """
        Set network offline/online

        Args:
            offline: True for offline, False for online
        """
        try:
            self.context.set_offline(offline)
            logger.info(f"Set network offline: {offline}")
        except Exception as e:
            logger.error(f"Error setting offline mode: {str(e)}")
            raise

    def set_geolocation(self, latitude: float, longitude: float, accuracy: float = 0) -> None:
        """
        Set geolocation

        Args:
            latitude: Latitude
            longitude: Longitude
            accuracy: Accuracy in meters
        """
        try:
            self.context.set_geolocation({
                'latitude': latitude,
                'longitude': longitude,
                'accuracy': accuracy
            })
            logger.info(f"Set geolocation: ({latitude}, {longitude})")
        except Exception as e:
            logger.error(f"Error setting geolocation: {str(e)}")
            raise

    def grant_permissions(self, permissions: List[str]) -> None:
        """
        Grant browser permissions

        Args:
            permissions: List of permissions (e.g., ['geolocation', 'notifications'])
        """
        try:
            self.context.grant_permissions(permissions)
            logger.info(f"Granted permissions: {permissions}")
        except Exception as e:
            logger.error(f"Error granting permissions: {str(e)}")
            raise

    def set_extra_http_headers(self, headers: Dict[str, str]) -> None:
        """
        Set extra HTTP headers

        Args:
            headers: Dictionary of headers
        """
        try:
            self.context.set_extra_http_headers(headers)
            logger.info("Set extra HTTP headers")
        except Exception as e:
            logger.error(f"Error setting HTTP headers: {str(e)}")
            raise

        # ==================== Viewport Operations ====================

    def set_viewport_size(self, width: int, height: int) -> None:
        """
        Set viewport size

        Args:
            width: Viewport width
            height: Viewport height
        """
        try:
            self.page.set_viewport_size({'width': width, 'height': height})
            logger.info(f"Set viewport size: {width}x{height}")
        except Exception as e:
            logger.error(f"Error setting viewport size: {str(e)}")
            raise

    def get_viewport_size(self) -> Dict[str, int]:
        """
        Get current viewport size

        Returns:
            Dictionary with 'width' and 'height'
        """
        try:
            size = self.page.viewport_size
            logger.info(f"Viewport size: {size}")
            return size
        except Exception as e:
            logger.error(f"Error getting viewport size: {str(e)}")
            return {'width': 0, 'height': 0}

        # ==================== Utility Methods ====================

    def get_page_content(self) -> str:
        """
        Get full page HTML content

        Returns:
            Page HTML
        """
        try:
            content = self.page.content()
            logger.info("Got page content")
            return content
        except Exception as e:
            logger.error(f"Error getting page content: {str(e)}")
            return ""

    def set_default_timeout(self, timeout: int) -> None:
        """
        Set default timeout for all operations

        Args:
            timeout: Timeout in milliseconds
        """
        self.default_timeout = timeout
        if self.page:
            self.page.set_default_timeout(timeout)
        logger.info(f"Set default timeout: {timeout}ms")

    def set_default_navigation_timeout(self, timeout: int) -> None:
        """
        Set default navigation timeout

        Args:
            timeout: Timeout in milliseconds
        """
        if self.page:
            self.page.set_default_navigation_timeout(timeout)
        logger.info(f"Set default navigation timeout: {timeout}ms")

    def bring_to_front(self) -> None:
        """Bring page to front"""
        try:
            self.page.bring_to_front()
            logger.info("Brought page to front")
        except Exception as e:
            logger.error(f"Error bringing page to front: {str(e)}")

    def emulate_media(self, media_type: str = None, color_scheme: str = None) -> None:
        """
        Emulate media type and/or color scheme

        Args:
            media_type: 'screen' or 'print'
            color_scheme: 'light', 'dark', or 'no-preference'
        """
        try:
            self.page.emulate_media(media=media_type, color_scheme=color_scheme)
            logger.info(f"Emulated media: {media_type}, color scheme: {color_scheme}")
        except Exception as e:
            logger.error(f"Error emulating media: {str(e)}")
            raise

    def pause(self) -> None:
        """Pause execution (for debugging)"""
        try:
            self.page.pause()
            logger.info("Execution paused")
        except Exception as e:
            logger.error(f"Error pausing: {str(e)}")

