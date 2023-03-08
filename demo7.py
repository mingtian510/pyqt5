import xlrd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QHeaderView, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class ExcelSearcher(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建主窗口
        self.setWindowTitle("Excel Searcher")
        self.setGeometry(100, 100, 800, 600)

        # 创建搜索框和按钮
        search_label = QLabel("Search Term:")
        self.search_line_edit = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(search_button)

        search_widget = QWidget()
        search_widget.setLayout(search_layout)

        # 创建表格视图
        self.table_view = QTableView()

        # 将搜索框和表格视图添加到主窗口中
        main_layout = QVBoxLayout()
        main_layout.addWidget(search_widget)
        main_layout.addWidget(self.table_view)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

        # 初始化模型
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)

    def search(self):
        # 获取搜索关键字
        search_term = self.search_line_edit.text()

        # 打开 Excel 文件并获取第一个工作表
        workbook = xlrd.open_workbook("example.xlsx")
        worksheet = workbook.sheet_by_index(0)

        # 获取表头信息
        header_row = worksheet.row(0)
        header_names = [cell.value for cell in header_row]

        # 获取指定列的数据
        target_column = header_names.index("Name")
        target_data = [worksheet.cell_value(row, target_column) for row in range(1, worksheet.nrows)]

        # 查找符合搜索关键字的行
        matching_rows = []
        for row_index, row_data in enumerate(worksheet.get_rows()):
            if row_index == 0:  # 跳过表头行
                continue
            if search_term in target_data[row_index - 1]:
                matching_rows.append([cell.value for cell in row_data])

        # 将匹配的行数据添加到模型中
        self.model.clear()
        self.model.setHorizontalHeaderLabels(header_names)
        for row_data in matching_rows:
            row_items = [QStandardItem(item) for item in row_data]
            self.model.appendRow(row_items)

        # 调整表格视图的列宽和行高
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.verticalHeader().setDefaultSectionSize(20)

if __name__ == "__main__":
    app = QApplication([])
    window = ExcelSearcher()
    window.show()
    app.exec_()
