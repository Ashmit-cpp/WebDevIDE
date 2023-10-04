from PyQt5.QtPrintSupport import QPrintDialog

from stx_highlight import *
from widget.custom_bar import MyBar
from widget.tab_widget import TabWidget
from widget.edit_toolbar import create_edit_toolbar
from widget.file_toolbar import create_file_toolbar
from utility_functions import *


class MainWindow(QMainWindow):
    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(''' color: white; background-color : #202020; ''')
        self.setMinimumSize(400, 400)
        self.titleBar = MyBar(self)
        self.main_window_functions = MainWindowFunctions(self)
        # self.setStyleSheet("border : 3px dashed blue;")
        self.editor = QPlainTextEdit()
        self.Dock = QDockWidget(" Browser", self)
        self.Dock.setMinimumWidth(550)
        self.Dock.setStyleSheet('''  QDockWidget::title  {   padding: 14px;  } ''')
        self.Dock.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.Dock.setWidget(Browser(self))
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.Dock)
        self.setFont(QFont('Seoge UI', 12))
        self.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.resize(640, self.titleBar.height() + 480)
        self.setGeometry(100, 100, 600, 400)
        self.path = None
        self.TabW = TabWidget(self)
        self.TabW.tabCloseRequested.connect(self.close_current_tab)
        self.TabW.currentChanged.connect(self.current_tab_changed)
        self.pages = []
        self.main_window_functions.add_tab()
        self.tabButton = QToolButton(self)
        self.tabButton.setText('+')
        font = self.tabButton.font()
        font.setBold(True)
        self.tabButton.setFont(font)
        self.TabW.setCornerWidget(self.tabButton)
        self.tabButton.clicked.connect(self.main_window_functions.add_tab)

        layout = QVBoxLayout()
        layout.addWidget(self.TabW)
        layout.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")
        self.status.setMinimumHeight(40)
        self.status.setStyleSheet('''
                    color: #B8B8B8;
                    background-color : #1F1F1F;
                    padding: 5px;
             ''')
        #file_toolbar
        self.file_toolbar = create_file_toolbar(self)
        self.edit_toolbar = create_edit_toolbar(self)
        self.update_title()
        self.show()

    def add_tab(self):
        #self.pages.append(self.editor)
        self.text = QPlainTextEdit()
        self.text.setStyleSheet(" background-color: #272727;"
                                  "border: 100px;"
                                  "font: 22px; "
                                  "font-family: JetBrains Mono;"
                                  )
        self.pages.append(self.text)
        self.highlighter = Highlighter(self.text.document())
        self.TabW.addTab(self.pages[-1], "Untitled")
        self.TabW.setCurrentIndex(len(self.pages) - 1)

    def close_current_tab(self, i):
        if self.TabW.count() < 2:
            return
        self.TabW.removeTab(i)

    def UpdateColor(self, value):
        self.CurrW = self.TabW.currentWidget()
        self.CurrW.setStyleSheet(
            f'QWidget {{background-color: rgb({value},{value},{value}); color: rgb({255},{255},{255}); font: 22px; font-family: JetBrains Mono; }}')

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    # action called by file open action
    def file_open(self):
        # getting path and bool value
        self.CurrW = self.TabW.currentWidget()
        self.highlighter = Highlighter(self.CurrW.document())
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                              "Text documents (*.txt);All files (*.*)")

        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()

            except Exception as e:

                self.dialog_critical(str(e))
            else:
                self.path = path
                self.CurrW.setPlainText(text)
                self.update_title()

    # action called by file save action
    def file_save(self):
        if self.path is None:
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                                              "All files (*.*)")

        if not path:
            return

        self._save_to_path(path)

    # save to path method
    def _save_to_path(self, path):
        self.CurrW = self.TabW.currentWidget()

        text = self.CurrW.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)

        # if error occurs
        except Exception as e:
            self.dialog_critical(str(e))

        # else do this
        else:
            self.path = path
            self.update_title()

    # action called by print
    def file_print(self):
        self.CurrW = self.TabW.currentWidget()
        dlg = QPrintDialog()
        if dlg.exec_():
            self.CurrW.print_(dlg.printer())

    # update title method
    def update_title(self):
        if self.path is not None:
            self.TabW.setTabText(self.TabW.currentIndex(), os.path.basename(self.path))
            self.setWindowTitle("%s - IDE" % os.path.basename(self.path))
        else:
            self.TabW.setTabText(self.TabW.currentIndex(), "Untitled")
            self.setWindowTitle("Untitled - IDE")

    def edit_toggle_wrap(self):
        self.CurrW = self.TabW.currentWidget()
        if self.CurrW.lineWrapMode() == QPlainTextEdit.WidgetWidth:
            self.CurrW.setLineWrapMode(QPlainTextEdit.NoWrap)
        else:
            self.CurrW.setLineWrapMode(QPlainTextEdit.WidgetWidth)

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            self.titleBar.windowStateChanged(self.windowState())

    def resizeEvent(self, event):
        self.titleBar.resize(self.width(), self.titleBar.height())

    def current_tab_changed(self, i):
        self.CurrW = self.TabW.currentWidget()
        self.setWindowTitle(self.TabW.tabText(self.TabW.currentIndex()))
        self.highlighter = Highlighter(self.CurrW.document())

