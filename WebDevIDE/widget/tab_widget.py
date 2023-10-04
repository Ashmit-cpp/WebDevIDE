# tab_widget.py
from PyQt5.QtWidgets import QTabWidget


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.setMinimumWidth(400)

        self.setStyleSheet("""
            QTabWidget {
                background-color: #202020;
                padding: 5px;
                font: 20px 'Roboto';
            }
            QTabWidget::pane {
                top: 1px;
                bottom: 1px;
                background: #202020;
            }
            QTabBar::tab {
                background: #202020;
                padding: 9px;
                padding-right: 50px;
            }
            QTabBar::close-button {
                image: url(images/close_white_18dp.svg);
                subcontrol-position: right;
            }
            QTabBar::close-button:hover {
                background: #4b7fad;
            }
            QTabBar::tab:selected {
                background: #272727;
                margin-bottom: -1px;
            }
        """)
        self.setTabsClosable(True)
        self.setMovable(True)
