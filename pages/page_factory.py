from utils.page import *
from utils.pageobject_support import callable_find_by as by


class BaiduPage(BasicPage):

    search_box = by(id_="kw")
    search_button = by(id_='su')

    def search(self, keywords):
        self.search_box().send_keys(keywords)
        self.search_button().click()
