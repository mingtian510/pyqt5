import sys
from PyQt5.QtWidgets import QApplication, QLabel, QTableView, QVBoxLayout, QLineEdit, QHBoxLayout, QWidget, \
    QMainWindow, QAction, QDialog, QDialogButtonBox, QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QFontMetrics
from PyQt5.QtCore import QSettings, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from logzero import logger
import xlrd
from PyQt5.QtGui import QPainter


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


class LineNumberArea(QTextEdit):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("background-color: #e0e0e0;")

    def update_width(self):
        width = self.fontMetrics().width(str(self.editor.blockCount())) + 10
        self.setFixedWidth(width)

    def update(self, rect, dy):
        if dy:
            self.scroll(0, dy)
        else:
            self.updateGeometry()
        if rect.contains(self.editor.viewport().rect()):
            self.editor.setViewportMargins(self.width(), 0, 0, 0)

        super().update(rect)

    def paintEvent(self, event):
        self.editor.setViewportMargins(self.width(), 0, 0, 0)
        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        painter = QPainter(self.viewport())
        painter.fillRect(event.rect(), Qt.lightGray)
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        current_height = self.fontMetrics().height()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, int(top), int(self.width()) - 5, current_height, Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1
        painter.end()
        super().paintEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_name = None
        self.settings = QSettings('Youkia', 'Config_Filter')
        if len(self.settings.value('config_dict')):
            self.config_dict = self.settings.value('config_dict')
        else:
            self.config_dict = {}
        # Create main widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 前端配置数据
        self.client_id_label = QLabel("前端id标题：")
        self.client_id_text = QLineEdit()

        self.client_field_label = QLabel("数据列标题")
        self.client_field_text = QLineEdit()
        if self.config_name:
            self.client_id_text.setText(self.config_dict[self.config_name]['client_id_col'])
            self.client_field_text.setText(self.config_dict[self.config_name]['client_field_col'])
        # self.client_field_text.textChanged.connect(self.set_search_col)
        self.client_field_text.setPlaceholderText("请输入前端配置表所需数据列标题")
        self.client_field_text.setAlignment(Qt.AlignCenter)

        # Create table view
        self.table_view_client = QTableView()
        self.table_view_server = QPlainTextEdit()
        # 添加行号显示
        self.line_number_area = LineNumberArea(self.table_view_server)
        self.table_view_server.blockCountChanged.connect(self.line_number_area.update_width)
        self.table_view_server.updateRequest.connect(self.line_number_area.update)
        self.line_number_area.update_width()


        self.table_view_server.setReadOnly(True)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_col_label)
        search_layout.addWidget(self.search_col_edit)
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_edit)

        table_layout = QHBoxLayout()
        table_layout.addWidget(self.table_view_client)
        table_layout.addWidget(self.line_number_area)
        table_layout.addWidget(self.table_view_server)

        main_layout = QVBoxLayout(central_widget)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(table_layout)

        self.statusBar()

        # # 创建打开文件的动作
        # openFile = QAction('打开', self)
        # openFile.setShortcut('Ctrl+O')

        # 创建设置配置文件的动作
        setclientFilePath = QAction('设置配置表路径', self)
        setclientFilePath.setShortcut('Ctrl+O')
        setclientFilePath.triggered.connect(self.set_config_file_path)

        # 创建菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        # fileMenu.addAction(openFile)
        fileMenu.addAction(setclientFilePath)

        self.init_local_data()

        # Set window properties
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('demo2.ico'))
        self.setWindowTitle("表格筛选")

    def init_table(self, file_path, file_type):
        if file_type == 'client':
            # 设置表格视图属性
            self.table_view_client.setSortingEnabled(True)
            self.table_view_client.setEditTriggers(QTableView.NoEditTriggers)
            self.table_view_client.setSelectionBehavior(QTableView.SelectRows)
            self.table_view_client.setSelectionMode(QTableView.SingleSelection)
            if file_path.endswith('.txt'):
                with open(r'' + file_path, 'r', encoding='UTF-8') as f:
                    try:
                        content = f.read()
                    except Exception as e:
                        self.statusBar().showMessage("文件读取失败：" + str(e))
                    _list = content.split('\n')
                    title_row = _list[2].split("\t")
                    # title_row = [i for i in title_row if i.strip() != ""]
                    self.model = QStandardItemModel(len(_list) - 2, len(title_row))
                    self.model.setHorizontalHeaderLabels(title_row)
                    self.table_view_client.setModel(self.model)

                    # 在表格控件中显示列内容
                    try:
                        for m, val in enumerate(_list[2:]):
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
                title_row = work_sheet.row_values(1)
                self.model = QStandardItemModel(nrows - 2, ncols)
                self.model.setHorizontalHeaderLabels(title_row)
                self.table_view_client.setModel(self.model)

                # 在表格控件中显示列内容
                try:
                    for n in range(2, nrows):
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
                self.table_view_client.setModel(self.filter_model)

                self.filter_model.setFilterColumn(self.search_column)  # 设置过滤列为对应列
                # self.filter_model.setFilterRegExp(QRegExp('2'))

                # 连接搜索框的文本变化信号到过滤器模型的过滤正则表达式槽函数
                self.search_edit.textChanged.connect(self.filter_model.setFilterRegExp)
            except Exception as e:
                self.statusBar().showMessage("设置过滤模型失败：" + str(e))

        elif file_type == 'server':
            try:
                if file_path.endswith('.cfg'):
                    with open(r'' + file_path, 'r', encoding='UTF-8') as f:
                        try:
                            content = f.read()
                        except Exception as e:
                            self.statusBar().showMessage("文件读取失败：" + str(e))
                        # _list = content.split('\n')
                        self.table_view_server.setPlainText(content)
                        # title_row = [i for i in title_row if i.strip() != ""]
                        # try:
                        #     for m, val in enumerate(_list[2:]):
                        #         if val:
                        #             # val 为每行的数据
                        #             cell_val_list = val.split("\t")
                        #             for i, cell in enumerate(cell_val_list):
                        #                 item = QStandardItem(str(cell))
                        #                 self.model.setItem(m, i, item)
                        #         else:
                        #             continue
                        # except Exception as e:
                        #     self.statusBar().showMessage("初始化表格数据失败：" + str(e))
            except Exception as e:
                self.statusBar().showMessage("初始化后台表数据失败：" + str(e))

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

    def set_config_file_path(self):
        # 创建一个对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("设置配置表路径")

        # 创建一个垂直布局
        layout = QVBoxLayout(dialog)

        # 创建配置表名字标签和文本框
        config_name_label = QLabel("自定义配置表名：", dialog)
        layout.addWidget(config_name_label)
        config_name_textEdit = QLineEdit(dialog)
        layout.addWidget(config_name_textEdit)

        # 创建前端路径标签和文本框
        client_label = QLabel("前端路径：", dialog)
        layout.addWidget(client_label)
        client_textEdit = QLineEdit(dialog)
        layout.addWidget(client_textEdit)

        # 创建后端路径标签和文本框
        server_label = QLabel("前端路径：", dialog)
        layout.addWidget(server_label)
        server_textEdit = QLineEdit(dialog)
        layout.addWidget(server_textEdit)

        # 创建一个按钮盒子
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        layout.addWidget(buttonBox)

        # 显示对话框
        if dialog.exec_() == QDialog.Accepted:
            try:
                client_path = client_textEdit.text()
                server_path = server_textEdit.text()
                logger.info(self.config_dict)
                client_field_col = 0
                client_id_col = 0
                server_pos_start_str = ''
                server_pos_end_str = ''
                server_id_re = ''
                server_field_re = ''
                config_data = dict(
                    client_path=client_path,
                    client_id_col=client_id_col,
                    client_field_col=client_field_col,
                    server_path=server_path,
                    server_pos_start_str=server_pos_start_str,
                    server_pos_end_str=server_pos_end_str,
                    server_id_re=server_id_re,
                    server_field_re=server_field_re
                )
                self.config_dict[config_name_textEdit.text()] = config_data
                self.settings.setValue('config_dict', self.config_dict)
            except Exception as e:
                self.statusBar().showMessage(str(e))

    def init_local_data(self):
        client_config_path = self.settings.value('client_config_path')
        if client_config_path:
            self.init_table(client_config_path, 'client')
            try:
                self.model
            except Exception as e:
                self.statusBar().showMessage("表格读取失败： " + str(e))
            self.init_search_col()
        server_config_path = self.settings.value('server_config_path')
        if server_config_path:
            self.init_table(server_config_path, 'server')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
