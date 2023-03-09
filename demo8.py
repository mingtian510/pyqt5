"""

打开应用自动打开指定路径文件并显示文件内容


"""
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from logzero import logger

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtGui import QTextCursor

class MainWindow(QMainWindow):
    def __init__(self, file_path):
        super().__init__()
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.load_file(file_path)

    def load_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='UTF-8') as file:
                file_contents = file.read()
                self.text_edit.setText(file_contents)
                self.text_edit.moveCursor(QTextCursor.Start)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(r'C:\Users\admin\Desktop\ItemConfig.txt')
    window.show()
    sys.exit(app.exec_())
