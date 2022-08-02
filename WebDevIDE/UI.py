from PyQt5.QtWidgets import QWidget
from Modules import *
from Browser import *
from Highlight import *

class MainWindow(QMainWindow):
    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(''' color: white; background-color : #202020; ''')
        self.setMinimumSize(400, 400)
        self.titleBar = MyBar(self)

        # self.setStyleSheet("border : 3px dashed blue;")
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
        self.TabW = QTabWidget(self)
        self.TabW.setMinimumWidth(400)

        self.editor = QPlainTextEdit()
        self.TabW.setStyleSheet("""
                                  QTabWidget  {
                                        background-color: #202020;
                                        padding: 5px;
                                        font: 11px, 'Roboto ';
                                    }
                                        QTabWidget::pane {
                                            top:1px; 
                                            bottom:1px;
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
        self.TabW.setTabsClosable(True)
        self.TabW.setMovable(True)
        self.TabW.tabCloseRequested.connect(self.close_current_tab)
        self.TabW.currentChanged.connect(self.current_tab_changed)
        self.pages = []
        self.add_tab()
        self.tabButton = QToolButton(self)
        self.tabButton.setText('+')
        font = self.tabButton.font()
        font.setBold(True)
        self.tabButton.setFont(font)
        self.TabW.setCornerWidget(self.tabButton)
        self.tabButton.clicked.connect(self.add_tab)

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

        file_toolbar = QToolBar("File")
        file_toolbar.setStyleSheet('''
                background-color: #202020;
                padding: 10px;
                padding-left: 3px;
                font: 7pt, 'Segoe UI ';
            ''')
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, file_toolbar)

        # creating a file menu
        file_menu = self.menuBar().addMenu("&File")
        self.menuBar().setStyleSheet("""
               QMenuBar {
                        background-color: #202020;
                        padding: 5px;
                        font: 11px, 'Segoe UI ';
                    }
                    QMenuBar::item {
                        padding: 7px 15px;
                        background-color: #202020;
                        color: rgb(255,255,255);  
                        border-radius: 5px;
                    }
                    QMenuBar::item:selected {    
                        background-color: rgb(42, 130, 218);
                    }
                    QMenuBar::item:pressed {
                        background-color: rgb(30, 98, 166);
                    }
                 """)

        add_tab_action = QAction(QIcon("images/add_white_18dp.svg"), "New Tab", self)
        add_tab_action.setStatusTip("New Tab")
        add_tab_action.triggered.connect(self.add_tab)
        file_menu.addAction(add_tab_action)
        file_toolbar.addAction(add_tab_action)
        file_toolbar.addSeparator()

        # adding action to the open file
        open_file_action = QAction(QIcon("images/file_open_white_18dp.svg"), "Open", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon("images/save_white_18dp.svg"), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon("images/save_as_white_18dp.svg"), "Save As", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon("images/print_white_18dp.svg"), "Print", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, edit_toolbar)

        edit_menu = self.menuBar().addMenu("&Edit")
        edit_toolbar.setStyleSheet('''
                        background-color: #202020;
                        padding: 10px;
                        padding-left: 3px;
                        font: 7pt, 'Segoe UI ';

                    ''')

        # undo action
        undo_action = QAction(QIcon("images/undo_white_18dp.svg"), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)

        # adding this to tool and menu bar
        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon("images/redo_white_18dp.svg"), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)

        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        cut_action = QAction(QIcon("images/content_cut_white_18dp.svg"), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)

        # adding this to menu and tool bar
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)
        copy_action = QAction(QIcon("images/content_copy_white_18dp.svg"), "Copy", self)
        copy_action.setStatusTip("Copy selected text")

        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        # paste action
        paste_action = QAction(QIcon("images/content_paste_white_18dp.svg"), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)

        # adding this to menu and tool bar
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)
        select_action = QAction(QIcon("images/select-all.png"), "Select all", self)
        select_action.setStatusTip("Select all text")
        self.CurrW = self.TabW.currentWidget()

        #select_action.triggered.connect(QKeySequence("Ctrl+A"))

        # adding this to menu and tool bar
        edit_toolbar.addAction(select_action)
        edit_menu.addAction(select_action)

        wrap_action = QAction("Wrap text to window", self)
        wrap_action.setStatusTip("Check to wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        # adding it to edit menu not to the tool bar
        edit_menu.addAction(wrap_action)
        slide = QSlider(Qt.Vertical)
        slide.setRange(0, 70)
        slide.setValue(40)
        slide.setMaximumWidth(300)
        slide.valueChanged.connect(self.UpdateColor)
        edit_toolbar.addWidget(slide)
        edit_toolbar.addSeparator()

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
        print(value)
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
        self.TabW.setTabText(self.TabW.currentIndex() ,"%s" % (os.path.basename(self.path)
                                                      if self.path else "Untitled "))
        self.setWindowTitle("%s - IDE" % ((self.path)
                                                      if self.path else "Untitled "))

    def edit_toggle_wrap(self):
        self.CurrW = self.TabW.currentWidget()
        self.CurrW.setLineWrapMode(1 if self.CurrW.lineWrapMode() == 0 else 0)

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            self.titleBar.windowStateChanged(self.windowState())

    def resizeEvent(self, event):
        self.titleBar.resize(self.width(), self.titleBar.height())

    def current_tab_changed(self, i):
        self.CurrW = self.TabW.currentWidget()
        self.setWindowTitle(self.TabW.tabText(self.TabW.currentIndex()))
        self.highlighter = Highlighter(self.CurrW.document())

        #self.CurrW = self.TabW.currentWidget()
        #self.triggered.connect(self.CurrW.selectAll)
