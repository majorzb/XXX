import sys,os
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MolecularEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Molecular Editor")
        self.setGeometry(100, 100, 800, 600)

        # 创建一个WebEngineView来嵌入JSME编辑器
        self.web_view = QWebEngineView()
        jsme_html = os.path.join(os.path.dirname(__file__), 'jsme.html')
        self.web_view.load(QUrl.fromLocalFile(jsme_html))
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)  # 禁用右键菜单
        self.web_view.page().profile().clearHttpCache()
        self.web_view.page().profile().clearAllVisitedLinks()

        # 创建一个按钮来获取绘制的分子
        self.get_molecule_button = QPushButton("Get Molecule")
        self.get_molecule_button.clicked.connect(self.getMolecule)

        # 创建一个布局
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        layout.addWidget(self.get_molecule_button)

        # 创建一个容器窗口
        container = QWidget()
        container.setLayout(layout)

        # 将容器窗口设置为主窗口的中央部分
        self.setCentralWidget(container)

    def getMolecule(self):
        # 通过JavaScript与JSME交互来获取绘制的分子结构
        script = """
        var mol = var glutathione_smiles;
        mol;
        """
        self.web_view.page().runJavaScript(script, self.handleMoleculeResult)

    def handleMoleculeResult(self, result):
        if result:
            print("Molecule Structure:")
            print(result)
        else:
            print("No molecule structure found.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MolecularEditor()
    window.show()
    sys.exit(app.exec_())


