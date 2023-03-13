from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QTextEdit
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = QPlainTextEdit()
        self.setCentralWidget(self.text_edit)

        # 添加行号显示
        self.line_number_area = LineNumberArea(self.text_edit)
        self.text_edit.blockCountChanged.connect(self.line_number_area.update_width)
        self.text_edit.updateRequest.connect(self.line_number_area.update)
        self.line_number_area.update_width()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("表格筛选")
        self.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(), self.line_number_area.width(), cr.height())


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
                painter.drawText(0, top, self.width() - 5, current_height, Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1
        painter.end()
        super().paintEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())