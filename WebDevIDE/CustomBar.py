# importing required libraries
from PyQt5.QtWidgets import QWidget

from Modules import *

class MyBar(QWidget):
    clickPos = None

    def __init__(self, parent):
        super(MyBar, self).__init__(parent)
        self.setAutoFillBackground(True)
        self.setFixedSize(16777215, 40)
        palette = self.palette()
        palette.setColor(palette.Window, QColor('#202020'))
        self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addStretch()

        self.title = QLabel(self, alignment=Qt.AlignBottom)
        self.title.setStyleSheet('''
                color: white;
                padding-left: 22px;
                font: 7pt, 'Segoe UI ';

            ''')

        btn_size = QSize(60, 40)
        for target in ('min', 'normal', 'max', 'close'):
            btn = QToolButton(self, focusPolicy=Qt.NoFocus)
            layout.addWidget(btn)
            btn.setFixedSize(btn_size)
            btn.setIcon(QIcon("images/icon_" + target + ".svg"))

            if target == 'close':
                colorNormal = '#202020'
                colorHover = '#C42B1C'
            else:
                colorNormal = '#202020'
                colorHover = '#2D2D2D'
            btn.setStyleSheet('''
                QToolButton {{
                    border: 0px solid;
                    background-color: #202020;
                }}
                QToolButton:hover {{
                    background-color: #2D2D2D;
                }}
            '''.format(colorNormal, colorHover))

            signal = getattr(self, target + 'Clicked')
            btn.clicked.connect(signal)

            setattr(self, target + 'Button', btn)

        self.normalButton.hide()

        self.updateTitle(parent.windowTitle())
        parent.windowTitleChanged.connect(self.updateTitle)

    def updateTitle(self, title=None):
        if title is None:
            title = self.window().windowTitle()
        width = self.title.width()
        width -= self.style().pixelMetric(QStyle.PM_LayoutHorizontalSpacing) * 2
        self.title.setText(self.fontMetrics().elidedText(
            title, Qt.ElideRight, width))

    def windowStateChanged(self, state):
        self.normalButton.setVisible(state == Qt.WindowMaximized)
        self.maxButton.setVisible(state != Qt.WindowMaximized)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickPos = event.windowPos().toPoint()

    def mouseMoveEvent(self, event):
        if self.clickPos is not None:
            self.window().move(event.globalPos() - self.clickPos)

    def mouseReleaseEvent(self, QMouseEvent):
        self.clickPos = None

    def closeClicked(self):
        self.window().close()

    def maxClicked(self):
        self.window().showMaximized()

    def normalClicked(self):
        self.window().showNormal()

    def minClicked(self):
        self.window().showMinimized()

    def resizeEvent(self, event):
        self.title.resize(self.minButton.x(), self.height())
        self.updateTitle()
