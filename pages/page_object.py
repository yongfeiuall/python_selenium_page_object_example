from utils.page import *

driver = webdriver.Ie()
class BaiduPage(BasicPage):

    search_box = ('id', 'kw')
    search_button = ('id', 'su')

    def search(self, keywords):
        self.input_text(self.search_box, keywords)
        self.click_element(self.search_button)

class TestIE(BasicPage):


    search_box = ('id', 'kw')
    search_button = ('id', 'su')

    def ie(self):
        self.open_page("http://www.baidu.com")