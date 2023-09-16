from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QLabel, QWidget, QPushButton, QGridLayout
import sys
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("批量导入示例")
        label = QLabel()
        label.setToolTip("This is a tooltip.")
        label.setStatusTip("This is a status tip.")
        label.setWhatsThis("This is a detailed description of the label.")



if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())