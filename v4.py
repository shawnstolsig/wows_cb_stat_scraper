# import bs4 as bs
# import json
# import sys
# import urllib.request
# from PyQt5.QtWebEngineWidgets import QWebEnginePage
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QUrl

# class Page(QWebEnginePage):
#     def __init__(self, url):
#         self.app = QApplication(sys.argv)
#         QWebEnginePage.__init__(self)
#         self.html = ''
#         self.loadFinished.connect(self._on_load_finished)
#         self.load(QUrl(url))
#         self.app.exec_()

#     def _on_load_finished(self):
#         self.html = self.toHtml(self.Callable)
#         print('Load finished')

#     def Callable(self, html_str):
#         self.html = html_str
#         self.app.quit()


# page = Page('worldofwarships.com')
# # soup = bs.BeautifulSoup(page.html, 'html.parser')
# input('enter when ready')
# page.load(QUrl('https://clans.worldofwarships.com/clans/wows/ladder/api/battles/?team=1'))
# input('enter when loaded')


import sys
import json
import bs4 as bs
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
web = QWebEngineView()
web.load(QUrl("https://worldofwarships.com"))
web.show()

input("enter when ready")

web.load(QUrl("https://clans.worldofwarships.com/clans/wows/ladder/api/battles/?team=1"))

input("enter once loaded")





# get a QWebEnginePage with:
p = web.page()



newDictionary = json.loads(web.page().grab())
print(newDictionary)
