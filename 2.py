from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QColor, QLinearGradient


class CustomGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundBrush(self.createGradientBackground())

        # 添加背景图片
        background_image = QPixmap("title.png")
        background_item = QGraphicsPixmapItem(background_image)
        self.addItem(background_item)

    def createGradientBackground(self):
        gradient = QLinearGradient(0, 0, 100, 0)
        gradient.setColorAt(0, QColor(23,58,103))  # 渐变起始颜色
        gradient.setColorAt(1, QColor(184,249,255))  # 渐变结束颜色
        return gradient


if __name__ == '__main__':
    app = QApplication([])

    # 创建 QGraphicsView 和 QGraphicsScene
    view = QGraphicsView()
    scene = CustomGraphicsScene()
    view.setScene(scene)

    view.show()
    app.exec()









