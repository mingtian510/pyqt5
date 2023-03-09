from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5.QtGui import QColor
import sys
"""
搜索表格指定内容
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建 QTableWidget 并填充数据
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(3)
        self.table.setHorizontalHeaderLabels(['Name', 'Age', 'Gender'])
        self.table.setItem(0, 0, QTableWidgetItem('Alice'))
        self.table.setItem(0, 1, QTableWidgetItem('20'))
        self.table.setItem(0, 2, QTableWidgetItem('Female'))
        self.table.setItem(1, 0, QTableWidgetItem('Bob'))
        self.table.setItem(1, 1, QTableWidgetItem('25'))
        self.table.setItem(1, 2, QTableWidgetItem('Male'))
        self.table.setItem(2, 0, QTableWidgetItem('Charlie'))
        self.table.setItem(2, 1, QTableWidgetItem('30'))
        self.table.setItem(2, 2, QTableWidgetItem('Male'))

        # 在窗口中显示 QTableWidget
        self.setCentralWidget(self.table)

        # 创建搜索框
        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.search_table)
        self.statusBar().addWidget(self.search_box)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('读取Excel指定列内容')
        self.show()

    def search_table(self, keyword):

        # 清除之前的标记
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                self.table.item(i, j).setBackground(QColor('white'))

        # 遍历 QTableWidget
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if item is not None and keyword.lower() in item.text().lower():
                    # 匹配成功，标记该单元格
                    item.setBackground(QColor('yellow'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())