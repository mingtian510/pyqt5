import sys
from PyQt5.QtWidgets import QApplication, QLabel, QTableView, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QWidget, \
    QMainWindow, \
    QTableWidget, QHeaderView, QTableWidgetItem, QAction, QFileDialog, QDialog, QDialogButtonBox, QFormLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QIcon
from PyQt5.QtCore import QSettings, Qt, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from logzero import logger

# 要重写QSortFilterProxyModel类
class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filter_column = 1  # 设置默认过滤列为第二列

    def setFilterColumn(self, column):
        self.filter_column = column

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, self.filter_column, source_parent)
        data = self.sourceModel().data(index)
        if self.filterRegExp().indexIn(data) != -1:
            return True
        else:
            return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a table view and set the model
        self.tableView = QTableView()
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)



        # Add some data to the model
        for row in range(5):
            for column in range(5):
                if column == 4:
                    column = 9
                item = QStandardItem("({},{})".format(row, column))
                self.model.setItem(row, column, item)

        # Set the proxy model to the table view
        self.proxyModel = SortFilterProxyModel()
        self.proxyModel.setSourceModel(self.model)
        self.tableView.setModel(self.proxyModel)
        self.proxyModel.setFilterKeyColumn(1)  # 设置过滤列为第二列
        self.proxyModel.setFilterRegExp(QRegExp('2'))

        # Add a line edit to filter the data
        self.lineEdit = QLineEdit()
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.tableView)
        # self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)

        # Add the table view and line edit to the main window

        self.setCentralWidget(centralWidget)

    def on_lineEdit_textChanged(self, text):
        # self.proxyModel.setFilterRegExp(text)
        self.proxyModel.setFilterByColumn(QRegExp(text, Qt.CaseSensitive, QRegExp.FixedString))

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
