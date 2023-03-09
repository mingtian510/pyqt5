"""
pyqt5 如何设置和修改数据，每次应用打开显示保存好的数据

"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QLineEdit
from PyQt5.QtCore import QSettings
from logzero import logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        # self.statusBar().addWidget(self.label)
        self.label.move(200, 100)
        self.load_data()
        self.create_button()
        self.create_text()

    def load_data(self):
        settings = QSettings('MyCompany', 'MyApp')
        my_data = settings.value('my_data', 'default_value')
        self.label.setText(my_data)

    def save_data(self, my_data):
        logger.info(my_data)
        settings = QSettings('MyCompany', 'MyApp')
        settings.setValue('my_data', my_data)
        self.label.setText(my_data)

    def create_button(self):
        button = QPushButton('Update Data1', self)
        button.clicked.connect(self.update_data)
        button.move(10, 10)

    def create_text(self):
        self.text_box = QLineEdit()
        self.statusBar().addWidget(self.text_box)
        # self.text_box.textChanged.connect(self.search_table)

    def update_data(self):
        logger.info(self.text_box.text())
        # my_data = 'New Value'
        self.save_data(self.text_box.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
