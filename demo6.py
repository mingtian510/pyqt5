import sys
import xlrd
from PyQt5.QtWidgets import QApplication, QLabel, QTableView, QPushButton, QVBoxLayout,  QLineEdit, QHBoxLayout, QWidget,  QMainWindow, \
    QTableWidget, QHeaderView, QTableWidgetItem, QAction, QFileDialog, QDialog, QDialogButtonBox, qApp
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QIcon
from PyQt5.QtCore import QSettings
from logzero import logger

class MainView(QWidget):
    pass

class MainWindow(QMainWindow):

    def __init__(self):
        self.book = None
        self.sheet = None
        # self.file_path = None
        super().__init__()
        self.statusBar()
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('读取Excel指定列内容')
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        try:
            self.search_label = QLabel('Search:')
            self.search_edit = QLineEdit()
            self.search_edit.textChanged.connect(self.search_table)
            # self.table = QTableWidget()
            self.table = QTableView()
            # self.setCentralWidget(self.table)

            search_layout = QHBoxLayout(central_widget)
            search_layout.addWidget(self.search_label)
            search_layout.addWidget(self.search_edit)

            main_layout = QVBoxLayout()
            main_layout.addLayout(search_layout)
            main_layout.addWidget(self.table)

            self.setLayout(main_layout)


            # 创建打开文件的动作
            openFile = QAction('打开', self)
            openFile.setShortcut('Ctrl+O')
            openFile.triggered.connect(self.fileDialog)


            # 创建设置配置文件的动作
            setFilePath = QAction('设置文件路径', self)
            setFilePath.triggered.connect(self.set_file_path)

            # 创建菜单栏
            menubar = self.menuBar()
            fileMenu = menubar.addMenu('文件')
            fileMenu.addAction(openFile)
            fileMenu.addAction(setFilePath)
        except Exception as e:
            self.statusBar().showMessage(str(e))

        # self.statusBar().addWidget(self.search_box)
        self.load_path_data()
        # 创建表格控件
        self.show()

    # 打开文件对话框
    def fileDialog(self):

        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.xls *.xlsx *.txt)')
        # 如果用户选择了文件，则读取文件内容并在 QTextEdit 中展示
        if filename:
            self.load_config_data(filename)

    # 加载指定路径的文件数据，展示在主界面中
    def load_config_data(self, file_path):
        # windows 复制路径时，开头会自带\\u202a
        # file_path = file_path.strip(r'\u202a')
        try:
            with open(r''+file_path, 'r', encoding='UTF-8') as f:
                try:
                    content = f.read()
                except Exception as e:
                    logger.info(str(e))
                _list = content.split('\n')
                title_row = _list[1].split("\t")
                # self.table.setColumnCount(len(first_row))
                # self.table.setRowCount(len(_list))
                self.model = QStandardItemModel(len(title_row), len(_list))
                self.model.setHorizontalHeaderLabels(title_row)
                self.table.setModel(self.model)
                # self.table = QStandardItemModel(len(title_row), len(_list))
                # self.table.setHorizontalHeaderLabels(title_row)
                # 在表格控件中显示列内容
                for m, val in enumerate(_list[1:]):
                    # val 为每行的数据
                    cell_val_list = val.split("\t")
                    logger.info(cell_val_list)
                    for i, cell in enumerate(cell_val_list):
                        item = QStandardItem(str(cell))
                        self.model.setItem(m, i, item)
                # 在表格控件中显示列内容
                # for m, val in enumerate(_list):
                #     # val 为每行的数据
                #     cell_val_list = val.split("\t")
                #     for i, cell in enumerate(cell_val_list):
                #         item = QTableWidgetItem(str(cell))
                #         self.table.setItem(m, i, item)
        except Exception as e:
            self.statusBar().showMessage(str(e))

    # 搜索表格
    def search_table(self, keyword):
        try:
            # 清除之前的标记
            for i in range(self.table.rowCount()):
                for j in range(self.table.columnCount()):
                    self.table.item(i, j).setBackground(QColor('white'))
        except Exception as e:
            pass
        if keyword:
            # 遍历 QTableWidget
            for i in range(self.table.rowCount()):
                for j in range(self.table.columnCount()):
                    item = self.table.item(i, j)
                    if item is not None and keyword.lower() in item.text().lower():
                        # 匹配成功，标记该单元格
                        item.setBackground(QColor('yellow'))

    # 设置文件路径
    def set_file_path(self):
        # 创建一个对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("Set Data")

        # 创建一个垂直布局
        layout = QVBoxLayout(dialog)

        # 创建标签和文本框
        label = QLabel("Enter data:", dialog)
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
            settings = QSettings('MyCompany', 'MyApp')
            settings.setValue('item_path', data)
            self.load_config_data(settings.value('item_path'))

    # 初始化设置好的配置文件数据
    def load_path_data(self):
        settings = QSettings('MyCompany', 'MyApp')
        my_data = settings.value('item_path')
        logger.info(my_data)
        if my_data:
        # self.file_path.setText(my_data)
            self.load_config_data(my_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
