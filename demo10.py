from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QAction, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import csv
import sys

class MyTable(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)

        self.setColumnCount(columns)
        self.setRowCount(rows)
        self.setHorizontalHeaderLabels(['Name', 'Age', 'Country'])

        # Add a context menu with "Add", "Delete" and "Save" options
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        add_action = QAction(QIcon('add.png'), 'Add', self)
        add_action.triggered.connect(self.add_row)
        delete_action = QAction(QIcon('delete.png'), 'Delete', self)
        delete_action.triggered.connect(self.delete_row)
        save_action = QAction(QIcon('save.png'), 'Save', self)
        save_action.triggered.connect(self.save_data)
        self.addAction(add_action)
        self.addAction(delete_action)
        self.addAction(save_action)

    def add_row(self):
        row_position = self.rowCount()
        self.insertRow(row_position)

    def delete_row(self):
        current_row = self.currentRow()
        self.removeRow(current_row)

    def save_data(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV(*.csv)')
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in range(self.rowCount()):
                row_data = []
                for column in range(self.columnCount()):
                    item = self.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                writer.writerow(row_data)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('QTableWidget Example')
        self.setGeometry(100, 100, 500, 500)

        # Create a QTableWidget and set it as the central widget
        self.table = MyTable(0, 3)
        self.setCentralWidget(self.table)

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
