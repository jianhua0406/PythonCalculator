import sys
import clipboard
from PyQt5.QtGui import QKeyEvent, QContextMenuEvent
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QLabel, QPushButton, QMainWindow, \
    QSizePolicy, QMenu, QAction, qApp
from qtconsole.qt import QtCore

from calculate import calculate_string

"""
todo : 
1.增加复制和粘贴功能 OK
2.增加历史记录功能
3.计算功能添加 OK
4.增加按键直接管用功能 OK
5.增加菜单功能 OK
6.增加删除功能 OK
7.增加复杂计算功能
"""


class ScreenWidget(QLabel):
    def __init__(self):
        super().__init__()

    def add(self, text):
        self.setText(self.text() + text)


class CalculatorWidget(QMainWindow):
    prepare_to_clear = False
    button_texts = (
        ('7', '8', '9', '/', 'C', 'Del'),
        ('4', '5', '6', '*', '('),
        ('1', '2', '3', '-', ')'),
        ('0', '.', '%', '+', '='),
    )
    key_to_button_text={
        QtCore.Qt.Key_0:'0',
        QtCore.Qt.Key_1:'1',
        QtCore.Qt.Key_2:'2',
        QtCore.Qt.Key_3:'3',
        QtCore.Qt.Key_4:'4',
        QtCore.Qt.Key_5:'5',
        QtCore.Qt.Key_6:'6',
        QtCore.Qt.Key_7:'7',
        QtCore.Qt.Key_8:'8',
        QtCore.Qt.Key_9:'9',
        QtCore.Qt.Key_Return:'=',
        QtCore.Qt.Key_Enter:'=',
        QtCore.Qt.Key_Backspace: 'Del',
        QtCore.Qt.Key_ParenLeft: '(',
        QtCore.Qt.Key_ParenRight: ')',
        QtCore.Qt.Key_Period: '.',
        QtCore.Qt.Key_C: 'C',
        QtCore.Qt.Key_Plus:'+',
        QtCore.Qt.Key_Minus:'-',
        QtCore.Qt.Key_Asterisk: '*',
        QtCore.Qt.Key_Slash: '/',
        QtCore.Qt.Key_Percent: '%',
    }
    button_texts_flatten = [text for texts in button_texts for text in texts]

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 200, 300)
        self.statusBar()
        self.init_UI()
        self.init_menu()
        self.init_menubar()

    def init_menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        exit_act = QAction('Exit', self)
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)
        file_menu.addAction(exit_act)

        edit_menu = menubar.addMenu('Edit')

        copy_act = QAction('Copy', self)
        copy_act.setStatusTip('Copy from clipboard')
        copy_act.triggered.connect(self.copy_fun)
        edit_menu.addAction(copy_act)

        paste_act = QAction('Paste', self)
        paste_act.setStatusTip('Paste to clipboard')
        paste_act.triggered.connect(self.paste_fun)
        edit_menu.addAction(paste_act)

    def init_menu(self):
        self.menu = QMenu()
        self.menu_copy = self.menu.addAction('copy')
        self.menu_paste = self.menu.addAction('paste')

    def init_UI(self):
        v_layout = QVBoxLayout()
        # calculate screen
        self.screen = ScreenWidget()
        v_layout.addWidget(self.screen, 2)
        # number or operator button
        grid_layout = QGridLayout()
        self.buttons = []
        for x, texts in enumerate(self.button_texts):
            for y, text in enumerate(texts):
                button = QPushButton(text)
                # add button in grid
                grid_layout.addWidget(button, x, y)
                # add buttons to buttons collection
                self.buttons.append(button)
                # add button clicked callback
                button.clicked.connect(self.click_callback)
                # make button's size expand
                button.setSizePolicy(
                    QSizePolicy.Expanding,
                    QSizePolicy.Expanding)
                button.setMinimumWidth(40)
        v_layout.addLayout(grid_layout, 3)
        self.setWindowTitle('Calculator')
        mainWidget = QWidget()
        mainWidget.setLayout(v_layout)
        self.setCentralWidget(mainWidget)
        self.show()

    def click_callback(self):
        sender = self.sender()
        text = sender.text()

        self.input_character(text)
        self.statusBar().showMessage('press button "%s"' % text)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        # 键盘的左边的“=”是“QtCore.Qt.Key_Return”，右边是“QtCore.Qt.Key_Enter”
        if key in self.key_to_button_text:
            key=self.key_to_button_text[key]
            self.input_character(key)
            self.statusBar().showMessage('press key "%s"' % key)

    def contextMenuEvent(self, event: QContextMenuEvent):
        action = self.menu.exec_(self.mapToGlobal(event.pos()))
        if action == self.menu_copy:
            self.copy_fun()
        elif action == self.menu_paste:
            self.paste_fun()

    def paste_fun(self):
        text = clipboard.paste()
        if text != '' and 'C' not in text and '=' not in text \
                and all([char in self.button_texts_flatten for char in text]):
            self.screen.setText(text)
            self.statusBar().showMessage('paste successfully')
        else:
            self.statusBar().showMessage('paste failed')

    def copy_fun(self):
        if self.screen.text() != '':
            clipboard.copy(self.screen.text())
            self.statusBar().showMessage('copy successfully')
        else:
            self.statusBar().showMessage('copy failed')

    def input_character(self, text):
        if self.prepare_to_clear:
            self.prepare_to_clear = False
            self.screen.clear()
        if text == 'C':
            self.screen.clear()
        elif text == '=':
            if self.screen.text() != '':
                self.screen.add('=%d' % calculate_string(self.screen.text()))
                self.prepare_to_clear = True
        elif text=='Del':
            if self.screen.text() != '':
                self.screen.setText(self.screen.text()[:-1])
        else:
            self.screen.add(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = CalculatorWidget()
    sys.exit(app.exec_())
