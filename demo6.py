import sys
import xlrd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QAction, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建表格控件
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)

        # 创建打开文件的动作
        openFile = QAction('打开', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.showDialog)

        # 创建菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('读取Excel指定列内容')
        self.show()

    def showDialog(self):
        # 打开文件对话框
        fname = QFileDialog.getOpenFileName(self, '打开文件', '.', 'Excel files (*.xls *.xlsx)')

        if fname[0]:
            # 打开 Excel 文件并获取指定列内容
            book = xlrd.open_workbook(fname[0])
            sheet = book.sheet_by_index(0)
            column_index = 0  # 指定读取的列号
            column_values = sheet.col_values(column_index)

            # 在表格控件中显示列内容
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setRowCount(len(column_values))
            for i, val in enumerate(column_values):
                item = QTableWidgetItem(str(val))
                self.tableWidget.setItem(i, 0, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
