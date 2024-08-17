from widget.browser_widget import *


def create_edit_toolbar(main_window):
    edit_toolbar = QToolBar("Edit")
    main_window.addToolBar(Qt.ToolBarArea.LeftToolBarArea, edit_toolbar)

    edit_menu = main_window.menuBar().addMenu("&Edit")
    edit_toolbar.setStyleSheet('''
        background-color: #202020;
        padding: 10px;
        padding-left: 3px;
        font: 7pt, 'Segoe UI ';
    ''')

    # Undo action
    undo_action = QAction(QIcon("./images/undo_white_18dp.svg"), "Undo", main_window)
    undo_action.setStatusTip("Undo last change")
    undo_action.triggered.connect(main_window.editor.undo)
    edit_toolbar.addAction(undo_action)
    edit_menu.addAction(undo_action)

    # Redo action
    redo_action = QAction(QIcon("./images/redo_white_18dp.svg"), "Redo", main_window)
    redo_action.setStatusTip("Redo last change")
    redo_action.triggered.connect(main_window.editor.redo)
    edit_toolbar.addAction(redo_action)
    edit_menu.addAction(redo_action)

    # Cut action
    cut_action = QAction(QIcon("./images/content_cut_white_18dp.svg"), "Cut", main_window)
    cut_action.setStatusTip("Cut selected text")
    cut_action.triggered.connect(main_window.editor.cut)
    edit_toolbar.addAction(cut_action)
    edit_menu.addAction(cut_action)

    # Copy action
    copy_action = QAction(QIcon("./images/content_copy_white_18dp.svg"), "Copy", main_window)
    copy_action.setStatusTip("Copy selected text")
    copy_action.triggered.connect(main_window.editor.copy)
    edit_toolbar.addAction(copy_action)
    edit_menu.addAction(copy_action)

    # Paste action
    paste_action = QAction(QIcon("./images/content_paste_white_18dp.svg"), "Paste", main_window)
    paste_action.setStatusTip("Paste from clipboard")
    paste_action.triggered.connect(main_window.editor.paste)
    edit_toolbar.addAction(paste_action)
    edit_menu.addAction(paste_action)

    # Select all action
    select_action = QAction(QIcon("./images/select-all.png"), "Select all", main_window)
    select_action.setStatusTip("Select all text")
    select_action.triggered.connect(main_window.editor.selectAll)
    edit_toolbar.addAction(select_action)
    edit_menu.addAction(select_action)

    # Wrap text action
    wrap_action = QAction("Wrap text to window", main_window)
    wrap_action.setStatusTip("Check to wrap text to window")
    wrap_action.setCheckable(True)
    wrap_action.setChecked(True)
    wrap_action.triggered.connect(main_window.edit_toggle_wrap)
    edit_menu.addAction(wrap_action)

    # Slider
    slide = QSlider(Qt.Vertical)
    slide.setRange(0, 70)
    slide.setValue(40)
    slide.setMaximumWidth(300)
    slide.valueChanged.connect(main_window.UpdateColor)
    edit_toolbar.addWidget(slide)
    edit_toolbar.addSeparator()

    return edit_toolbar
