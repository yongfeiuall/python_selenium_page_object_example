from utils.page import *


class BaiduPage(BasicPage):

    search_box = ('id', 'kw')
    search_button = ('id', 'su')

    def search(self, keywords):
        self.input_text(self.search_box, keywords)
        self.click_element(self.search_button)
