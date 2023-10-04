from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *


class Browser(QWidget):
    def __init__(self, parent):
        super(Browser, self).__init__(parent)
        self.brlayout = QVBoxLayout()
        self.brlayout.setContentsMargins(10, 0, 10, 10)
        self.setLayout(self.brlayout)
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(30, 25))
        navtb.setStyleSheet("background-color: #282828;")
        self.brlayout.addWidget(navtb)

        # creating a QWebEngineView
        self.browser = QWebEngineView()
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.brlayout.addWidget(self.browser)

        back_btn = QAction(QIcon("images/arrow_back_white_18dp.svg"), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon("images/arrow_forward_white_18dp.svg"), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon("images/reload_white_18dp.svg"), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        navtb.addSeparator()

        # creating a line edit for the url
        self.urlbar = QLineEdit()
        self.urlbar.setStyleSheet('''
                                  height: 30px;
                                  font: 14px; 
                                  background-color: #202020;
                                  border-width: 1px;
                                  border-style: solid;
                                  border-color: #303030;
                                  ''')
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        open_btn = QAction(QIcon("images/open_in_new_white_18dp.svg"), "Open", self)
        open_btn.setStatusTip("Open File")
        open_btn.triggered.connect(self.open_new)
        navtb.addAction(open_btn)
        # adding stop action to the tool bar
        stop_btn = QAction(QIcon("images/close_white_18dp.svg"), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        self.show()

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("% s " % title)

    def open_new(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                              "Text documents (*.html);All files (*.*)")
        self.browser.setUrl(QUrl(path))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())

        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

