#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
1、创建基础视图
2、创建按钮，按钮tips
3、给按钮绑定事件
4、重写关闭按钮，增加提示弹窗
5、是窗口居中
"""

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QDesktopWidget,
                             QPushButton, QApplication, QMessageBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication
from logzero import logger


class Demo2(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 设置tips的字体
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('这是什么？')

        # 按钮
        btn_tips = QPushButton(QIcon('demo2.ico'), '按钮', self)
        btn_tips.setToolTip("这是 <b>tips</b> 按钮")
        btn_tips.resize(btn_tips.sizeHint())
        btn_tips.move(10, 10)

        # 关闭按钮
        btn_quit = QPushButton(QIcon('demo2.ico'), '关闭按钮', self)
        btn_quit.clicked.connect(QCoreApplication.instance().quit)
        btn_quit.setToolTip("这是 <b>关闭</b> 按钮")
        btn_quit.resize(btn_quit.sizeHint())
        btn_quit.move(100, 10)

        # 设置app的基础信息
        self.setGeometry(300, 300, 300, 220)

        # 设置居中打开
        self.center()
        self.setWindowTitle("demo2")
        self.setWindowIcon(QIcon('demo2.ico'))

        self.show()

    # 重写了关闭事件，函数名固定
    # 但是这里关闭事件仅限于窗口右上角，如果自己重新写了其他的关闭按钮 则不会触发。
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出标题', '确定退出？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        # 获取屏幕分辨率
        logger.info(QDesktopWidget().availableGeometry())
        logger.info(cp)
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #
    # w = QWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle('demo2')
    # w.show()
    ex = Demo2()

    sys.exit(app.exec_())
