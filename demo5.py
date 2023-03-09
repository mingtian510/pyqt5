"""
事件和信号

1、signals
2、重写事件
3、事件对象
4、事件发送

"""


import sys

import logzero
from PyQt5.QtWidgets import QWidget, QLCDNumber, QSlider, QVBoxLayout, QApplication, QLabel, QPushButton, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

class Example(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        # 数字移动展示
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)

        # 鼠标移动事件展示
        x = 0,
        y = 0
        self.text = "x: {}, y: {}".format(x, y)
        self.label = QLabel(self.text, self)
        self.setMouseTracking(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)

        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('计数器')
        self.show()

    # 重写键盘事件
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        logzero.logger.info(e.key())
        if e.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        x = e.x()
        y = e.y()

        text = "x: {}, y: {}".format(x, y)
        self.label.setText(text)

    #  自定义button点击事件


class ExampleButton(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # button事件
        btn1 = QPushButton("button1", self)
        btn1.move(30, 50)
        btn2 = QPushButton("button2", self)
        btn2.move(150, 50)
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('按钮事件')
        self.show()

    def buttonClicked(self):

        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # ex = ExampleButton()
    sys.exit(app.exec_())