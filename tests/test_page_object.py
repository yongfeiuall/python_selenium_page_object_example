from pages.page_object import *
from conf.const import *


class TestPO():
    def test_baidu(self, start_browser):
        baidu = BaiduPage(start_browser)
        baidu.open_page(URL.baidu)
        baidu.search("selenium")
        start_browser.close()