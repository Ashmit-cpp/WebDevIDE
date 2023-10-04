# importing required libraries
import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow
from palette import get_custom_palette

# drivers code
if __name__ == '__main__':
    # creating PyQt5 application
    app = QApplication(sys.argv)
    app.setPalette(get_custom_palette())
    app.setStyle("Fusion")
    # creating a main window object
    mw = MainWindow()
    mw.showMaximized()
    sys.exit(app.exec_())
