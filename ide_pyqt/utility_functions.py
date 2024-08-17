from PyQt5.QtPrintSupport import QPrintDialog
from widget.browser_widget import *
import os
from stx_highlight import Highlighter


class MainWindowFunctions:
    def __init__(self, main_window):
        self.main_window = main_window

    def add_tab(self):
        text = QPlainTextEdit()
        text.setStyleSheet(" background-color: #272727;"
                           "border: 100px;"
                           "font: 22px; "
                           "font-family: JetBrains Mono;"
                           )
        self.main_window.pages.append(text)
        self.main_window.highlighter = Highlighter(text.document())
        self.main_window.TabW.addTab(self.main_window.pages[-1], "Untitled")
        self.main_window.TabW.setCurrentIndex(len(self.main_window.pages) - 1)

    def close_current_tab(self, i):
        if self.main_window.TabW.count() < 2:
            return
        self.main_window.TabW.removeTab(i)

    def update_color(self, value):
        self.main_window.CurrW = self.main_window.TabW.currentWidget()
        self.main_window.CurrW.setStyleSheet(
            f'QWidget {{background-color: rgb({value},{value},{value}); color: rgb({255},{255},{255}); font: 22px; font-family: JetBrains Mono; }}')

    def dialog_critical(self, s):
        dlg = QMessageBox(self.main_window)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        self.main_window.CurrW = self.main_window.TabW.currentWidget()
        self.main_window.highlighter = Highlighter(self.main_window.CurrW.document())

        path, _ = QFileDialog.getOpenFileName(self.main_window, "Open file", "",
                                              "Text documents (*.txt);All files (*.*)")

        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.main_window.path = path
                self.main_window.CurrW.setPlainText(text)
                self.main_window.update_title()

    def file_save(self):
        if self.main_window.path is None:
            return self.file_saveas()
        self._save_to_path(self.main_window.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self.main_window, "Save file", "",
                                              "All files (*.*)")
        if not path:
            return
        self._save_to_path(path)

    def _save_to_path(self, path):
        self.main_window.CurrW = self.main_window.TabW.currentWidget()
        text = self.main_window.CurrW.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.main_window.path = path
            self.main_window.update_title()

    def file_print(self):
        self.main_window.CurrW = self.main_window.TabW.currentWidget()
        dlg = QPrintDialog()
        if dlg.exec_():
            self.main_window.CurrW.print_(dlg.printer())

    def update_title(self):
        if self.main_window.path is not None:
            self.main_window.TabW.setTabText(self.main_window.TabW.currentIndex(), os.path.basename(self.main_window.path))
            self.main_window.setWindowTitle("%s - IDE" % os.path.basename(self.main_window.path))
        else:
            self.main_window.TabW.setTabText(self.main_window.TabW.currentIndex(), "Untitled")
            self.main_window.setWindowTitle("Untitled - IDE")

    def edit_toggle_wrap(self):
        self.main_window.CurrW = self.main_window.TabW.currentWidget()
        if self.main_window.CurrW.lineWrapMode() == QPlainTextEdit.WidgetWidth:
            self.main_window.CurrW.setLineWrapMode(QPlainTextEdit.NoWrap)
        else:
            self.main_window.CurrW.setLineWrapMode(QPlainTextEdit.WidgetWidth)

    def change_event(self, event):
        if event.type() == event.WindowStateChange:
            self.main_window.titleBar.windowStateChanged(self.main_window.windowState())

    def resize_event(self, event):
        self.main_window.titleBar.resize(self.main_window.width(), self.main_window.titleBar.height())

    def current_tab_changed(self, i):
        self.main_window.CurrW = self.main_window.TabW.currentWidget()
        self.main_window.setWindowTitle(self.main_window.TabW.tabText(self.main_window.TabW.currentIndex()))
        self.main_window.highlighter = Highlighter(self.main_window.CurrW.document())
