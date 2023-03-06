#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
1、状态栏
2、菜单栏
3、多级菜单
4、勾选菜单
5、右键菜单
6、工具栏
7、主窗口
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QMenu, QTextEdit
from PyQt5.QtGui import QIcon, QContextMenuEvent
from logzero import logger


class Demo3(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        # self.statusBar().showMessage('Ready')

        exitAct = QAction(QIcon('demo2.ico'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('退出应用')
        exitAct.triggered.connect(qApp.quit)

        select_file_Act = QAction(QIcon('demo2.ico'), '&文件', self)
        select_file_Act.setShortcut('Ctrl+S')
        select_file_Act.setStatusTip('选择文件')
        select_file_Act.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(select_file_Act)
        fileMenu.addAction(exitAct)

        # 多级菜单
        fileMenu_2 = menubar.addMenu('多级菜单')
        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)
        newAct = QAction('new', self)
        fileMenu_2.addAction(newAct)
        fileMenu_2.addMenu(impMenu)


        # 勾选菜单
        viewMenu = menubar.addMenu('勾选菜单')

        viewStatAct = QAction('View statusbar', self, checkable=True)
        viewStatAct.setStatusTip('切换显示状态栏')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)

        viewMenu.addAction(viewStatAct)

        # 工具栏
        exit_tool_act = QAction(QIcon('demo2.ico'), '退出应用', self)
        exit_tool_act.setShortcut("Ctrl+Q")
        exit_tool_act.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar("Exit")
        self.toolbar.addAction(exit_tool_act)

        self.setGeometry(500, 300, 550, 550)
        self.setWindowTitle('demo3')
        self.show()

        #  主界面设置为编辑框
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

    def toggleMenu(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    #  右键菜单
    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        cmenu = QMenu(self)

        newAct = cmenu.addAction("New")
        openAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")

        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
            qApp.quit()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Demo3()
    sys.exit(app.exec_())