"""
Base Page class for Page Object Model
Provides common page functionalities for all page objects
"""
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout
from typing import Optional, List, Dict, Any
import logging
import allure
import time
from core.utils.browser_utility import BrowserUtility


class BasePage:
    """
    Base page class providing common page functionalities
    All page object classes should inherit from this class
    """

    def __init__(self, browser_utility: BrowserUtility):
        """
        Initialize base page
        Args:
            browser_utility: BrowserUtility instance
        """
        self.browser_utility = browser_utility
        self.page: Page = browser_utility.page
        self.logger = logging.getLogger(self.__class__.__name__)
        self.default_timeout = 30000  # 30 seconds in milliseconds

    # ========================================================================
    # NAVIGATION METHODS
    # ========================================================================

    @allure.step("Navigate to page: {url}")
    def navigate_to(self, url: str, wait_until: str = "domcontentloaded"):
        """
        Navigate to specified URL
        Args:
            url: URL to navigate to
            wait_until: When to consider navigation complete
                       ('load', 'domcontentloaded', 'networkidle')
        """
        try:
            self.browser_utility.navigate_to(url)
            self.logger.info(f"Navigated to: {url}")
        except Exception as e:
            self.logger.error(f"Navigation failed to {url}: {e}")
            raise

    def refresh_page(self):
        """Refresh current page"""
        try:
            self.page.reload()
            self.logger.info("Page refreshed")
        except Exception as e:
            self.logger.error(f"Page refresh failed: {e}")
            raise

    def go_back(self):
        """Navigate back in browser history"""
        try:
            self.page.go_back()
            self.logger.info("Navigated back")
        except Exception as e:
            self.logger.error(f"Go back failed: {e}")
            raise

    def go_forward(self):
        """Navigate forward in browser history"""
        try:
            self.page.go_forward()
            self.logger.info("Navigated forward")
        except Exception as e:
            self.logger.error(f"Go forward failed: {e}")
            raise

    # ========================================================================
    # ELEMENT INTERACTION METHODS
    # ========================================================================

    @allure.step("Click element: {selector}")
    def click(self, selector: str, timeout: int = None):
        """
        Click on element
        Args:
            selector: Element selector
            timeout: Maximum wait time in milliseconds
        """
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.click(selector)
            self.logger.info(f"Clicked on element: {selector}")
        except Exception as e:
            self.logger.error(f"Click failed on {selector}: {e}")
            raise

    @allure.step("Double click element: {selector}")
    def double_click(self, selector: str, timeout: int = None):
        """Double click on element"""
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.dblclick(selector)
            self.logger.info(f"Double clicked on element: {selector}")
        except Exception as e:
            self.logger.error(f"Double click failed on {selector}: {e}")
            raise

    @allure.step("Right click element: {selector}")
    def right_click(self, selector: str, timeout: int = None):
        """Right click on element"""
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.click(selector, button="right")
            self.logger.info(f"Right clicked on element: {selector}")
        except Exception as e:
            self.logger.error(f"Right click failed on {selector}: {e}")
            raise

    @allure.step("Enter text '{text}' into: {selector}")
    def enter_text(self, selector: str, text: str, clear: bool = True, timeout: int = None):
        """
        Enter text in input field
        Args:
            selector: Element selector
            text: Text to enter
            clear: Clear field before entering text
            timeout: Maximum wait time
        """
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout)

            if clear:
                self.page.fill(selector, text)
            else:
                self.page.type(selector, text)

            self.logger.info(f"Entered text in {selector}")
        except Exception as e:
            self.logger.error(f"Enter text failed on {selector}: {e}")
            raise

    def clear_text(self, selector: str, timeout: int = None):
        """Clear text from input field"""
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.fill(selector, "")
            self.logger.info(f"Cleared text from {selector}")
        except Exception as e:
            self.logger.error(f"Clear text failed on {selector}: {e}")
            raise

    @allure.step("Press key: {key}")
    def press_key(self, key: str):
        """
        Press keyboard key
        Args:
            key: Key to press (e.g., 'Enter', 'Tab', 'Escape')
        """
        try:
            self.page.keyboard.press(key)
            self.logger.info(f"Pressed key: {key}")
        except Exception as e:
            self.logger.error(f"Press key failed for {key}: {e}")
            raise

    # ========================================================================
    # ELEMENT RETRIEVAL METHODS
    # ========================================================================

    @allure.step("Get text from element: {selector}")
    def get_text(self, selector: str, timeout: int = None) -> str:
        """
        Get text from element
        Args:
            selector: Element selector
            timeout: Maximum wait time
        Returns:
            Element text
        """
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout)
            text = self.page.text_content(selector)
            self.logger.info(f"Retrieved text from {selector}: {text}")
            return text if text else ""
        except Exception as e:
            self.logger.error(f"Get text failed on {selector}: {e}")
            raise

    def get_attribute(self, selector: str, attribute: str, timeout: int = None) -> Optional[str]:
        """
        Get element attribute value
        Args:
            selector: Element selector
            attribute: Attribute name
            timeout: Maximum wait time
        Returns:
            Attribute value
        """
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout)
            value = self.page.get_attribute(selector, attribute)
            self.logger.info(f"Retrieved attribute '{attribute}' from {selector}: {value}")
            return value
        except Exception as e:
            self.logger.error(f"Get attribute failed on {selector}: {e}")
            raise

    def get_all_texts(self, selector: str, timeout: int = None) -> List[str]:
        """
        Get text from all matching elements
        Args:
            selector: Element selector
            timeout: Maximum wait time
        Returns:
            List of texts
        """
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout)
            elements = self.page.query_selector_all(selector)
            texts = [element.text_content() for element in elements]
            self.logger.info(f"Retrieved {len(texts)} texts from {selector}")
            return texts
        except Exception as e:
            self.logger.error(f"Get all texts failed on {selector}: {e}")
            raise

    def get_element_count(self, selector: str) -> int:
        """
        Get count of matching elements
        Args:
            selector: Element selector
        Returns:
            Number of matching elements
        """
        try:
            count = self.page.locator(selector).count()
            self.logger.info(f"Found {count} elements matching {selector}")
            return count
        except Exception as e:
            self.logger.error(f"Get element count failed on {selector}: {e}")
            raise

    # ========================================================================
    # ELEMENT STATE METHODS
    # ========================================================================

    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if element is visible
        Args:
            selector: Element selector
            timeout: Maximum wait time
        Returns:
            True if visible, False otherwise
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            self.logger.info(f"Element is visible: {selector}")
            return True
        except:
            self.logger.debug(f"Element not visible: {selector}")
            return False

    def is_element_hidden(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is hidden"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state="hidden")
            return True
        except:
            return False

    def is_element_enabled(self, selector: str) -> bool:
        """Check if element is enabled"""
        try:
            return self.page.is_enabled(selector)
        except Exception as e:
            self.logger.error(f"is_element_enabled failed on {selector}: {e}")
            return False

    def is_element_disabled(self, selector: str) -> bool:
        """Check if element is disabled"""
        try:
            return self.page.is_disabled(selector)
        except Exception as e:
            self.logger.error(f"is_element_disabled failed on {selector}: {e}")
            return False

    def is_checkbox_checked(self, selector: str) -> bool:
        """Check if checkbox is checked"""
        try:
            return self.page.is_checked(selector)
        except Exception as e:
            self.logger.error(f"is_checkbox_checked failed on {selector}: {e}")
            return False

    # ========================================================================
    # WAIT METHODS
    # ========================================================================

    @allure.step("Wait for element: {selector}")
    def wait_for_element(self, selector: str, timeout: int = None, state: str = "visible"):
        """
        Wait for element to be in specified state
        Args:
            selector: Element selector
            timeout: Maximum wait time
            state: Element state ('attached', 'detached', 'visible', 'hidden')
        """
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout, state=state)
            self.logger.info(f"Element {selector} is {state}")
        except Exception as e:
            self.logger.error(f"Wait for element failed on {selector}: {e}")
            raise

    def wait_for_element_to_disappear(self, selector: str, timeout: int = None):
        """Wait for element to disappear"""
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout, state="hidden")
            self.logger.info(f"Element disappeared: {selector}")
        except Exception as e:
            self.logger.error(f"Wait for element to disappear failed on {selector}: {e}")
            raise

    def wait_for_url(self, url: str, timeout: int = None):
        """Wait for URL to match"""
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_url(url, timeout=timeout)
            self.logger.info(f"URL matched: {url}")
        except Exception as e:
            self.logger.error(f"Wait for URL failed: {e}")
            raise

    def wait_for_page_load(self, timeout: int = None):
        """Wait for page to load completely"""
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            self.logger.info("Page loaded completely")
        except Exception as e:
            self.logger.error(f"Wait for page load failed: {e}")
            raise

    def wait_for_specific_time(self, seconds: int):
        """
        Wait for specified seconds
        Args:
            seconds: Number of seconds to wait
        """
        time.sleep(seconds)
        self.logger.info(f"Waited for {seconds} seconds")

    # ========================================================================
    # DROPDOWN/SELECT METHODS
    # ========================================================================

    @allure.step("Select dropdown option: {value}")
    def select_dropdown_by_value(self, selector: str, value: str):
        """Select option from dropdown by value"""
        try:
            self.page.select_option(selector, value=value)
            self.logger.info(f"Selected option by value '{value}' from {selector}")
        except Exception as e:
            self.logger.error(f"Select dropdown failed on {selector}: {e}")
            raise

    def select_dropdown_by_label(self, selector: str, label: str):
        """Select option from dropdown by visible text"""
        try:
            self.page.select_option(selector, label=label)
            self.logger.info(f"Selected option by label '{label}' from {selector}")
        except Exception as e:
            self.logger.error(f"Select dropdown failed on {selector}: {e}")
            raise

    def select_dropdown_by_index(self, selector: str, index: int):
        """Select option from dropdown by index"""
        try:
            self.page.select_option(selector, index=index)
            self.logger.info(f"Selected option by index {index} from {selector}")
        except Exception as e:
            self.logger.error(f"Select dropdown failed on {selector}: {e}")
            raise

    # ========================================================================
    # CHECKBOX/RADIO METHODS
    # ========================================================================

    @allure.step("Check checkbox: {selector}")
    def check_checkbox(self, selector: str):
        """Check checkbox if not already checked"""
        try:
            if not self.page.is_checked(selector):
                self.page.check(selector)
                self.logger.info(f"Checked checkbox: {selector}")
            else:
                self.logger.info(f"Checkbox already checked: {selector}")
        except Exception as e:
            self.logger.error(f"Check checkbox failed on {selector}: {e}")
            raise

    @allure.step("Uncheck checkbox: {selector}")
    def uncheck_checkbox(self, selector: str):
        """Uncheck checkbox if checked"""
        try:
            if self.page.is_checked(selector):
                self.page.uncheck(selector)
                self.logger.info(f"Unchecked checkbox: {selector}")
            else:
                self.logger.info(f"Checkbox already unchecked: {selector}")
        except Exception as e:
            self.logger.error(f"Uncheck checkbox failed on {selector}: {e}")
            raise

    # ========================================================================
    # SCROLL METHODS
    # ========================================================================

    @allure.step("Scroll to element: {selector}")
    def scroll_to_element(self, selector: str):
        """Scroll to element"""
        try:
            self.page.locator(selector).scroll_into_view_if_needed()
            self.logger.info(f"Scrolled to element: {selector}")
        except Exception as e:
            self.logger.error(f"Scroll to element failed on {selector}: {e}")
            raise

    def scroll_to_top(self):
        """Scroll to top of page"""
        try:
            self.page.evaluate("window.scrollTo(0, 0)")
            self.logger.info("Scrolled to top of page")
        except Exception as e:
            self.logger.error(f"Scroll to top failed: {e}")
            raise

    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        try:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.logger.info("Scrolled to bottom of page")
        except Exception as e:
            self.logger.error(f"Scroll to bottom failed: {e}")
            raise

    def scroll_by_amount(self, x: int, y: int):
        """
        Scroll by specified amount
        Args:
            x: Horizontal scroll amount
            y: Vertical scroll amount
        """
        try:
            self.page.evaluate(f"window.scrollBy({x}, {y})")
            self.logger.info(f"Scrolled by x={x}, y={y}")
        except Exception as e:
            self.logger.error(f"Scroll by amount failed: {e}")
            raise

    # ========================================================================
    # FRAME/IFRAME METHODS
    # ========================================================================

    def switch_to_frame(self, frame_selector: str):
        """Switch to iframe"""
        try:
            frame = self.page.frame_locator(frame_selector)
            self.logger.info(f"Switched to frame: {frame_selector}")
            return frame
        except Exception as e:
            self.logger.error(f"Switch to frame failed: {e}")
            raise

    def switch_to_default_content(self):
        """Switch back to main content"""
        try:
            # In Playwright, this is handled automatically
            self.logger.info("Switched to default content")
        except Exception as e:
            self.logger.error(f"Switch to default content failed: {e}")
            raise

    # ========================================================================
    # JAVASCRIPT EXECUTION METHODS
    # ========================================================================

    def execute_javascript(self, script: str, *args) -> Any:
        """
        Execute JavaScript on page
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script
        Returns:
            Script execution result
        """
        try:
            result = self.page.evaluate(script, *args)
            self.logger.info(f"Executed JavaScript: {script[:50]}...")
            return result
        except Exception as e:
            self.logger.error(f"JavaScript execution failed: {e}")
            raise

    def highlight_element(self, selector: str):
        """Highlight element (useful for debugging)"""
        try:
            script = """
            (selector) => {
                const element = document.querySelector(selector);
                if (element) {
                    element.style.border = '3px solid red';
                    element.style.backgroundColor = 'yellow';
                }
            }
            """
            self.page.evaluate(script, selector)
            self.logger.info(f"Highlighted element: {selector}")
        except Exception as e:
            self.logger.error(f"Highlight element failed: {e}")

    # ========================================================================
    # ALERT/DIALOG METHODS
    # ========================================================================

    def accept_alert(self):
        """Accept alert dialog"""
        try:
            self.page.on("dialog", lambda dialog: dialog.accept())
            self.logger.info("Alert accepted")
        except Exception as e:
            self.logger.error(f"Accept alert failed: {e}")
            raise

    def dismiss_alert(self):
        """Dismiss alert dialog"""
        try:
            self.page.on("dialog", lambda dialog: dialog.dismiss())
            self.logger.info("Alert dismissed")
        except Exception as e:
            self.logger.error(f"Dismiss alert failed: {e}")
            raise

    def get_alert_text(self) -> str:
        """Get alert text"""
        alert_text = ""

        def handle_dialog(dialog):
            nonlocal alert_text
            alert_text = dialog.message
            dialog.accept()

        self.page.on("dialog", handle_dialog)
        return alert_text

    # ========================================================================
    # PAGE INFORMATION METHODS
    # ========================================================================

    def get_page_title(self) -> str:
        """Get page title"""
        try:
            title = self.page.title()
            self.logger.info(f"Page title: {title}")
            return title
        except Exception as e:
            self.logger.error(f"Get page title failed: {e}")
            raise

    def get_current_url(self) -> str:
        """Get current URL"""
        try:
            url = self.page.url
            self.logger.info(f"Current URL: {url}")
            return url
        except Exception as e:
            self.logger.error(f"Get current URL failed: {e}")
            raise

    def get_page_source(self) -> str:
        """Get page HTML source"""
        try:
            source = self.page.content()
            self.logger.info("Retrieved page source")
            return source
        except Exception as e:
            self.logger.error(f"Get page source failed: {e}")
            raise

    # ========================================================================
    # SCREENSHOT METHODS
    # ========================================================================

    def take_screenshot(self, filename: str = None) -> str:
        """
        Take screenshot
        Args:
            filename: Screenshot filename
        Returns:
            Path to screenshot
        """
        try:
            screenshot_path = self.browser_utility.take_screenshot(filename)
            return screenshot_path
        except Exception as e:
            self.logger.error(f"Take screenshot failed: {e}")
            raise

    def take_element_screenshot(self, selector: str, filename: str = None) -> str:
        """Take screenshot of specific element"""
        try:
            import os
            from datetime import datetime

            if not filename:
                filename = f"element_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

            screenshot_path = f"screenshots/{filename}"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

            self.page.locator(selector).screenshot(path=screenshot_path)
            self.logger.info(f"Element screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.logger.error(f"Take element screenshot failed: {e}")
            raise

    # ========================================================================
    # HOVER METHODS
    # ========================================================================

    @allure.step("Hover over element: {selector}")
    def hover(self, selector: str, timeout: int = None):
        """Hover over element"""
        try:
            timeout = timeout or self.default_timeout
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.hover(selector)
            self.logger.info(f"Hovered over element: {selector}")
        except Exception as e:
            self.logger.error(f"Hover failed on {selector}: {e}")
            raise

    # ========================================================================
    # DRAG AND DROP METHODS
    # ========================================================================

    @allure.step("Drag and drop from {source_selector} to {target_selector}")
    def drag_and_drop(self, source_selector: str, target_selector: str):
        """Drag and drop element"""
        try:
            self.page.drag_and_drop(source_selector, target_selector)
            self.logger.info(f"Dragged {source_selector} to {target_selector}")
        except Exception as e:
            self.logger.error(f"Drag and drop failed: {e}")
            raise

    # ========================================================================
    # FILE UPLOAD METHODS
    # ========================================================================

    @allure.step("Upload file: {file_path}")
    def upload_file(self, selector: str, file_path: str):
        """
        Upload file
        Args:
            selector: File input selector
            file_path: Path to file to upload
        """
        try:
            self.page.set_input_files(selector, file_path)
            self.logger.info(f"Uploaded file: {file_path}")
        except Exception as e:
            self.logger.error(f"File upload failed: {e}")
            raise

    def upload_multiple_files(self, selector: str, file_paths: List[str]):
        """Upload multiple files"""
        try:
            self.page.set_input_files(selector, file_paths)
            self.logger.info(f"Uploaded {len(file_paths)} files")
        except Exception as e:
            self.logger.error(f"Multiple file upload failed: {e}")
            raise

    # ========================================================================
    # COOKIE METHODS
    # ========================================================================

    def get_cookies(self) -> List[Dict]:
        """Get all cookies"""
        try:
            cookies = self.page.context.cookies()
            self.logger.info(f"Retrieved {len(cookies)} cookies")
            return cookies
        except Exception as e:
            self.logger.error(f"Get cookies failed: {e}")
            raise

    def add_cookie(self, cookie: Dict):
        """Add cookie"""
        try:
            self.page.context.add_cookies([cookie])
            self.logger.info(f"Added cookie: {cookie.get('name')}")
        except Exception as e:
            self.logger.error(f"Add cookie failed: {e}")
            raise

    def clear_cookies(self):
        """Clear all cookies"""
        try:
            self.page.context.clear_cookies()
            self.logger.info("Cleared all cookies")
        except Exception as e:
            self.logger.error(f"Clear cookies failed: {e}")
            raise

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def wait(self, seconds: int):
        """
        Wait for specified seconds
        Args:
            seconds: Number of seconds to wait
        """
        time.sleep(seconds)
        self.logger.info(f"Waited for {seconds} seconds")

    def get_viewport_size(self) -> Dict[str, int]:
        """Get viewport size"""
        try:
            size = self.page.viewport_size
            self.logger.info(f"Viewport size: {size}")
            return size
        except Exception as e:
            self.logger.error(f"Get viewport size failed: {e}")
            raise

    def set_viewport_size(self, width: int, height: int):
        """Set viewport size"""
        try:
            self.page.set_viewport_size({"width": width, "height": height})
            self.logger.info(f"Set viewport size to {width}x{height}")
        except Exception as e:
            self.logger.error(f"Set viewport size failed: {e}")
            raise
