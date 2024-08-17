from widget.browser_widget import *


def create_file_toolbar(main_window):
    file_toolbar = QToolBar("File")
    file_toolbar.setStyleSheet('''
            background-color: #202020;
            padding: 10px;
            padding-left: 3px;
            font: 7pt, 'Segoe UI';
        ''')
    main_window.addToolBar(Qt.ToolBarArea.LeftToolBarArea, file_toolbar)

    # Create and add actions to the file_toolbar here
    add_tab_action = QAction(QIcon("./images/add_white_18dp.svg"), "New Tab", main_window)
    add_tab_action.setStatusTip("New Tab")
    add_tab_action.triggered.connect(main_window.add_tab)
    file_toolbar.addAction(add_tab_action)
    file_toolbar.addSeparator()

    open_file_action = QAction(QIcon("./images/file_open_white_18dp.svg"), "Open", main_window)
    open_file_action.setStatusTip("Open file")
    open_file_action.triggered.connect(main_window.file_open)
    file_toolbar.addAction(open_file_action)

    save_file_action = QAction(QIcon("./images/save_white_18dp.svg"), "Save", main_window)
    save_file_action.setStatusTip("Save current page")
    save_file_action.triggered.connect(main_window.file_save)
    file_toolbar.addAction(save_file_action)

    saveas_file_action = QAction(QIcon("./images/save_as_white_18dp.svg"), "Save As", main_window)
    saveas_file_action.setStatusTip("Save current page to specified file")
    saveas_file_action.triggered.connect(main_window.file_saveas)
    file_toolbar.addAction(saveas_file_action)

    print_action = QAction(QIcon("./images/print_white_18dp.svg"), "Print", main_window)
    print_action.setStatusTip("Print current page")
    print_action.triggered.connect(main_window.file_print)
    file_toolbar.addAction(print_action)

    return file_toolbar
