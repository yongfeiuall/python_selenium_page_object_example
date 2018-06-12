import time
from selenium.common.exceptions import *
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

TIME_OUT = 5.0


class BasicPage(object):

    def __init__(self, driver):
        self.driver = driver

    def open_page(self, url):
        """**Description**::
                        open the page
        """
        self.driver.get(url)
        self.driver.maximize_window()

    def input_text(self, locator, value):
        """**Description**::
                Fill value to the element located by locator

        :param locator:The locator to locate the element.
        :param value:value to set to the element
        :return:
        """
        element = self._find_web_element(locator)
        element.send_keys(value)
        return self

    def get_text(self, locator):
        """**Description**::
                Get the text of the element identified by locator

        :param locator:The locator to locate the element.
        :return:The text of the element.
        """
        element = self._find_web_element(locator)
        return element.text

    def get_value(self, locator):
        """**Description**::
                Get the value of the element identified by locator

        :param locator:The locator to locate the element.
        :return:The value of the element.
        """
        element = self._find_web_element(locator)
        return element.value

    def get_attribute(self, locator, attribute_name):
        """**Description**::
                Gets the given attribute or property of the element.

        :param locator:The locator to locate the element.
        :param attribute_name:The attribute name to retrieve.
        :return:
        """
        element = self._find_web_element(locator, False)
        if not element:
            return None
        return element.get_attribute(attribute_name)

    def click_element(self, locator):
        """**Description**::
                Click element identified by locator

        :param locator:The locator to locate the element.
        :return:
        """
        element = self._find_web_element(locator)
        element.click()
        return self

    def is_visible(self, locator):
        """**Description**::
                Get the visibility of element identified by locator

        :param locator:The locator to locate the element.
        :return:
        """
        element = self._find_web_element(locator, False)
        if not element:
            return False
        return element.visible

    def is_enable(self, locator):
        """**Description**::
                Get the usability of element identified by locator

        :param locator:The locator to locate the element.
        :return:
        """
        element = self._find_web_element(locator, False)
        if not element:
            return False
        return element.is_enable()

    def is_clickable(self, locator):
        """**Description**::
                Check the element identified by locator is clickable

        :param locator:The locator to locate the element.
        :return:
        """
        element = self._find_web_element(locator, False)
        if not element:
            return False
        return element.is_enable() and element.visible

    def is_selected(self, locator):
        element = self._find_web_element(locator, False)
        if not element:
            return False
        return element.checked

    def select_by_values(self, locator, values=None):
        if not values:
            raise Exception('No value given.')
        element = self._find_web_element(locator)
        for value in values:
            element.select(value)
        return self

    def select_by_text(self, locator, texts=None):
        if not texts:
            raise Exception('No texts given.')
        element = self._find_web_element(locator)
        for text in texts:
            element.select_by_text(text)
        return self

    def select_by_index(self, locator, indexs=None):
        if not indexs:
            raise Exception('No texts given.')
        select_element = self._find_web_element(locator)
        for index in indexs:
            select_element.select_by_index(index)
        return self

    def element_should_be_visible(self, locator, message=None):
        if not self.is_visible(locator):
            if not message:
                message = 'Element %s should be visible, but it is not.' % locator[1]
            raise ElementNotVisibleException(message)

    def element_should_be_clickable(self, locator, message=None):
        if not self.is_clickable(locator):
            if not message:
                message = 'Element %s should be clickable, but it is not.' % locator[1]
            raise WebDriverException(message)

    def element_should_be_selected(self, locator, message=None):
        if not self.is_selected(locator):
            if not message:
                message = 'Element %s should be selected, but it is not.' % locator[1]
            raise WebDriverException(message)

    def wait_until_element_is_enable(self, locator, timeout=None, error=None):
        if not timeout:
            timeout = TIME_OUT

        def check_enabled():
            enabled = self.is_enable(locator)
            if enabled:
                return
            else:
                return error or "Element '%s' was not enabled in %s" % (locator[1], float(timeout))

        self._wait_until_no_error(timeout, check_enabled)

    def wait_until_element_is_clickable(self, locator, timeout=None, error=None):
        if not timeout:
            timeout = TIME_OUT

        def check_click_able():
            click_able = self.is_clickable(locator)
            if click_able:
                return
            else:
                return error or "Element '%s' was not enabled in %s seconds" % (locator[1], float(timeout))

        self._wait_until_no_error(timeout, check_click_able)
        return self

    def wait_until_element_is_not_clickable(self, locator, timeout=None, error=None):
        if not timeout:
            timeout = TIME_OUT

        def check_not_click_able():
            click_able = self.is_clickable(locator)
            if not click_able:
                return
            else:
                return error or "Element '%s' still clickable in %s seconds" % (locator[1], float(timeout))

        self._wait_until_no_error(timeout, check_not_click_able)

    def wait_until_element_is_visible(self, locator, timeout=None, error=None):
        """Waits until element specified with `locator` is visible.

        Fails if `timeout` expires before the element is visible.
        """
        if not timeout:
            timeout = TIME_OUT

        def check_visibility():
            visible = self.is_visible(locator)
            if visible:
                return
            else:
                return error or "Element '%s' was not visible in %s seconds" % (locator[1], float(timeout))

        self._wait_until_no_error(timeout, check_visibility)
        return self

    def wait_until_element_is_not_visible(self, locator, timeout=None, error=None):
        if not timeout:
            timeout = TIME_OUT

        def check_not_visibility():
            visible = self.is_visible(locator)
            if not visible:
                return
            else:
                return error or "Element '%s' was not visible in %s seconds" % (locator[1], float(timeout))

        self._wait_until_no_error(timeout, check_not_visibility)

    def wait_for_element_clickable_then_click_it(self, locator):
        if not self.is_clickable(locator):
            self.wait_until_element_is_clickable(locator, 120)
        self.click_element(locator)
        return self

    def wait_for_element_visible_then_click_it(self, locator):
        self.wait_until_element_is_visible(locator)
        self.repeat_click_until_element_not_visible(locator)
        return self

    def repeat_click_until_element_not_visible(self, locator):
        try_time = 2
        while self.is_visible(locator) and try_time <= 5:
            self.click_element(locator)
            time.sleep(try_time)
            try_time += 1
        return self

    def repeat_click_until_another_element_visible(self, clicked_locator, visible_locator):
        try_time = 2
        while self.is_visible(visible_locator) is False and try_time <= 5:
            self.click_element(clicked_locator)
            time.sleep(try_time)
            try_time += 1
        return self

    def mouse_over(self, locator):
        """**Description**::
                Performs a mouse over the element

        :param locator:The locator to locate the element.
        :return:
        """
        element = self._find_web_element(locator)
        element.mouse_over()
        return self

    def mouse_out(self, locator):
        """**Description**::
                Performs a mouse out the element

        :param locator:The locator to locate the element.
        :return:
        """
        element = self._find_web_element(locator)
        element.mouse_out()
        return self

    def double_click(self, locator):
        """
        Performs a double click in the element.
        """
        element = self._find_web_element(locator)
        element.double_click()
        return self

    def right_click(self, locator):
        """
        Performs a right click in the element.

        """
        element = self._find_web_element(locator)
        element.right_click()
        return self

    def click_element_at_coordinates(self, locator, xoffset=100, yoffset=100):
        """**Description**::
                Performs a mouse out the element

        :param locator:The locator to locate the element.
        :return:
        """
        element = self._find_web_element(locator)
        element.click_element_at_coordinates(xoffset, yoffset)
        return self

    def drag_and_drop(self, locator, droppable):
        """
        Performs drag a element to another elmenet.
        """
        element = self._find_web_element(locator)
        drop_element = self._find_web_element(droppable)
        element.drag_and_drop(element, drop_element)
        return self

    def _find_web_element(self, locator, raise_exception=True):
        element = self.driver.find_element(*locator)
        if not element and raise_exception:
            raise NoSuchElementException('Element %s not exist.' % locator[1])
        if not element:
            return None

        return element

    def _wait_until_no_error(self, timeout, wait_func, *args):
        if not timeout:
            timeout = TIME_OUT
        timeout = float(timeout)
        max_time = time.time() + timeout
        while True:
            timeout_error = wait_func(*args)
            if not timeout_error:
                return
            if time.time() > max_time:
                raise AssertionError(timeout_error)
            time.sleep(0.2)
