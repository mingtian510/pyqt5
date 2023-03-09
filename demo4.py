#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
布局管理
1、绝对定位
2、盒布局
3、栅格布局
4、制作提交反馈信息的布局
"""

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QGridLayout, QLineEdit, QTextEdit)
from logzero import logger

# 绝对定位
class ExampleAbsolute(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        lbl1 = QLabel('Zetcode', self)
        lbl1.move(15, 10)

        lbl2 = QLabel('tutorials', self)
        lbl2.move(35, 40)

        lbl3 = QLabel('for programmers', self)
        lbl3.move(55, 70)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute')
        self.show()



# 盒布局
class ExampleBox(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()


# 栅格布局
class ExampleGrid(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        positions = [(i, j) for i in range(5) for j in range(4)]

        for positions, name in zip(positions, names):
            logger.info(positions)
            logger.info(name)
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *positions)

        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()


# 制作提交反馈信息的布局
class ExampleCommit(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        title = QLabel('标题')
        author = QLabel('作者')
        content = QLabel('文本')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        contentEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1, 1, 4)
        # grid.addWidget(titleEdit, 1, 3)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1, 2, 4)
        # grid.addWidget(authorEdit, 2, 3)

        grid.addWidget(content, 4, 0)
        grid.addWidget(contentEdit, 4, 1, 4, 4)
        # grid.addWidget(contentEdit, 3, 3, 5, 3)

        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')

        grid.addWidget(okButton, 8, 3)
        grid.addWidget(cancelButton, 8, 4)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("content")
        self.show()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    # 绝对定位
    # ex = ExampleAbsolute()
    ex = ExampleBox()
    # ex = ExampleGrid()
    # ex = ExampleCommit()
    sys.exit(app.exec_())