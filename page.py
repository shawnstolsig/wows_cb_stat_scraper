from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import sys

class Page(QWebEnginePage):

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print(self.html)

    def Callable(self,html_str):
        self.html = html_str
        self.app.quit()

    # @staticmethod
    # def create_window():
    #     app = QApplication(sys.argv)
    #     web = QWebEngineView()
    #     web.load(QUrl("www.google.com"))
    #     web.show()

    #     sys.exit(app.exec_())
