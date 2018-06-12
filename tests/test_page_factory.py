from conf.const import *
from pages.page_factory import *


class TestPF():
    def test_baidu(self, start_browser):
        baidu = BaiduPage(start_browser)
        baidu.open_page(URL.baidu)
        baidu.search("selenium")
        start_browser.close()