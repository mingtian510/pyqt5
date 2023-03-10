import sys
from PyQt5.QtWidgets import QApplication, QLabel, QTableView, QVBoxLayout, QLineEdit, QHBoxLayout, QWidget, \
    QMainWindow, QAction, QDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from logzero import logger
import xlrd


# 要重写QSortFilterProxyModel类
class SortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filter_column = 0  # 设置默认过滤列为第一列

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
        self.search_column = 0
        self.settings = QSettings('Youkia', 'Config_Filter')
        # Create main widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create search box
        self.search_label = QLabel("搜索内容")
        self.search_edit = QLineEdit()
        self.search_col_label = QLabel("搜索列（输入标题）")
        self.search_col_edit = QLineEdit()
        self.search_col_edit.setText(self.settings.value('title_text'))
        self.search_col_edit.textChanged.connect(self.set_search_col)
        self.search_edit.setPlaceholderText("Search...")
        self.search_edit.setAlignment(Qt.AlignCenter)

        # Create table view
        self.table_view = QTableView()

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_col_label)
        search_layout.addWidget(self.search_col_edit)
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_edit)

        main_layout = QVBoxLayout(central_widget)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table_view)

        self.statusBar()

        # # 创建打开文件的动作
        # openFile = QAction('打开', self)
        # openFile.setShortcut('Ctrl+O')

        # 创建设置配置文件的动作
        setFilePath = QAction('设置读取文件路径', self)
        setFilePath.setShortcut('Ctrl+O')
        setFilePath.triggered.connect(self.set_file_path)

        # 创建菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        # fileMenu.addAction(openFile)
        fileMenu.addAction(setFilePath)

        self.init_local_data()

        # Set window properties
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('demo2.ico'))
        self.setWindowTitle("表格筛选")

    def init_table(self, file_path):
        # 设置表格视图属性
        self.table_view.setSortingEnabled(True)
        self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        if file_path.endswith('.txt'):
            with open(r'' + file_path, 'r', encoding='UTF-8') as f:
                try:
                    content = f.read()
                except Exception as e:
                    self.statusBar().showMessage("文件读取失败：" + str(e))
                _list = content.split('\n')
                title_row = _list[0].split("\t")
                # title_row = [i for i in title_row if i.strip() != ""]
                self.model = QStandardItemModel(len(_list), len(title_row))
                self.model.setHorizontalHeaderLabels(title_row)
                self.table_view.setModel(self.model)

                # 在表格控件中显示列内容
                try:
                    for m, val in enumerate(_list[1:]):
                        if val:
                            # val 为每行的数据
                            cell_val_list = val.split("\t")
                            for i, cell in enumerate(cell_val_list):
                                item = QStandardItem(str(cell))
                                self.model.setItem(m, i, item)
                        else:
                            continue
                except Exception as e:
                    self.statusBar().showMessage("初始化表格数据失败：" + str(e))
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls') or file_path.endswith('.xlsm'):
            workbook = xlrd.open_workbook(file_path)
            work_sheet = workbook.sheet_by_index(0)
            nrows = work_sheet.nrows
            ncols = work_sheet.ncols
            title_row = work_sheet.row_values(0)
            self.model = QStandardItemModel(nrows, ncols)
            self.model.setHorizontalHeaderLabels(title_row)
            self.table_view.setModel(self.model)

            # 在表格控件中显示列内容
            try:
                for n in range(1, nrows):
                    cell_val_list = work_sheet.row_values(n)
                    for i, cell in enumerate(cell_val_list):
                        c_type = work_sheet.cell(n, i).ctype
                        if c_type == 2 and cell % 1 == 0.0:  # 处理整数变为浮点数的情况， ctype为2且为浮点
                            cell = int(cell)
                        item = QStandardItem(str(cell))
                        self.model.setItem(n, i, item)
            except Exception as e:
                self.statusBar().showMessage("初始化表格数据失败：" + str(e))

        try:
            # 创建过滤器模型
            self.filter_model = SortFilterProxyModel()
            self.filter_model.setSourceModel(self.model)

            # 设置表格视图模型
            self.table_view.setModel(self.filter_model)

            self.filter_model.setFilterColumn(self.search_column)  # 设置过滤列为对应列
            # self.filter_model.setFilterRegExp(QRegExp('2'))

            # 连接搜索框的文本变化信号到过滤器模型的过滤正则表达式槽函数
            self.search_edit.textChanged.connect(self.filter_model.setFilterRegExp)
        except Exception as e:
            self.statusBar().showMessage("设置过滤模型失败：" + str(e))

    # 获取保存好的搜索title数据
    def init_search_col(self):
        title_text = self.settings.value('title_text')
        if title_text:
            try:
                for column in range(self.model.columnCount()):
                    if self.model.headerData(column, Qt.Horizontal) == title_text:
                        # 找到了，column 就是对应的列索引
                        self.search_column = column
                        self.filter_model.setFilterColumn(self.search_column)
                        self.statusBar().showMessage("找到对应列数据，请输入搜索内容")
                        break
                else:
                    # 没有找到
                    self.statusBar().showMessage("未找到对应列，请检查搜索列数据是否正确")
            except Exception as e:
                self.statusBar().showMessage("数据异常，请设置文件路径")

    def set_search_col(self):
        self.settings.setValue('title_text', self.search_col_edit.text())
        self.init_search_col()

    def set_file_path(self):
        # 创建一个对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("设置配置表路径")

        # 创建一个垂直布局
        layout = QVBoxLayout(dialog)

        # 创建标签和文本框
        label = QLabel("路径：", dialog)
        layout.addWidget(label)
        textEdit = QLineEdit(dialog)
        layout.addWidget(textEdit)

        # 创建一个按钮盒子
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        layout.addWidget(buttonBox)

        # 显示对话框
        if dialog.exec_() == QDialog.Accepted:
            data = textEdit.text()
            self.settings.setValue('item_path', data)
            self.init_table(self.settings.value('item_path'))

    def init_local_data(self):
        item_path = self.settings.value('item_path')
        if item_path:
            self.init_table(item_path)
            try:
                self.model
            except Exception as e:
                self.statusBar().showMessage("表格读取失败： " + str(e))
            self.init_search_col()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
