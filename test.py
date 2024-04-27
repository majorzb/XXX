from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import  QFileDialog,QScrollArea, QWidget, QFrame, QPlainTextEdit

import sys

from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import Draw
IPythonConsole.ipython_useSVG=False #如果想展示PNG请设置为FALSE

import pandas as pd
import io
import os

from two import Ui_MainWindow
from CIGIN.prediction import main as delt_g_main
from tox_21.prediction import main as tox_21_main
from tox_21.prediction import resource_path


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        global icon
        super(QMainWindow,self).__init__()
        self.setupUi(self)
        #设置窗口图标
        self.setWindowTitle('分子性质预测')
        icon = QIcon(resource_path("title.png"))
        self.setWindowIcon(icon)
        # 点击左边功能键，切换到相应界面
        self.pushButton.clicked.connect(self.display_page1)
        self.pushButton_2.clicked.connect(self.display_page2)
        self.pushButton_3.clicked.connect(self.display_page3)
        self.pushButton_6.clicked.connect(self.display_page4)
        #预测溶剂化自由能
        self.pushButton_5.clicked.connect(self.Delt_g)

        #预测tox_21毒性
        self.pushButton_4.clicked.connect(self.tox_21)

        #批量预测
        self.pushButton_8.clicked.connect(self.Batch_predict)
        #批量保存
        self.pushButton_9.clicked.connect(self.Batch_save)
        #批量导入
        self.pushButton_10.clicked.connect(self.Batch_import)


    def display_page1(self):
        self.stackedWidget.setCurrentIndex(1)
        self.frame.setStyleSheet("QFrame#frame{\n"
                                 "background-color:qlineargradient(x1:0,y0:1,x1:0,y1:1,stop:0 rgb(89,98,175), stop:1 rgb(72,155,219));\n"
                                 "border-radius:18px;}")

    def display_page2(self):
        self.stackedWidget.setCurrentIndex(2)
        self.frame.setStyleSheet("QFrame#frame{\n"
                                 "background-color:qlineargradient(x1:0,y0:1,x1:0,y1:1,stop:0 rgb(60,50,111), stop:1 rgb(192,182,246));\n"
                                 "border-radius:18px;}")

    def display_page3(self):
        self.stackedWidget.setCurrentIndex(0)
        self.frame.setStyleSheet("QFrame#frame{\n"
                                 "background-color:qlineargradient(x1:0,y0:1,x1:0,y1:1,stop:0 rgb(19,61,112), stop:1 rgb(54,124,173));\n"
                                 "border-radius:18px;}")

    def display_page4(self):
        self.stackedWidget.setCurrentIndex(3)
        self.frame.setStyleSheet("QFrame#frame{\n"
                                 "    background-color:qlineargradient(x1:0,y0:1,x1:0,y1:1,stop:0 rgb(19,61,112), stop:1 rgb(54,124,173));\n"
                                 "border-radius:18px;}")

    def Delt_g(self,):
        # 设置字体
        font = QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setFamily('宋体')
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # 允许滚动区域自适应大小
        #设置弹窗
        self.msg_box1 = QWidget()
        self.msg_box1.setWindowIcon(icon)
        self.msg_box1.setWindowTitle("result")
        self.msg_box1.resize(380, 500)
        self.frameg = QFrame(self)
        self.layout1 = QGridLayout(self.frameg)
        #读取溶质，溶剂smiles
        solute = self.lineEdit_2.text()
        solvent = self.lineEdit_3.text()

        if  any(c.isdigit() for c in solute) or  any(c.isdigit() for c in solvent):
            QMessageBox.warning(self, "提示", "请输入正确的smiles")
        elif not solute or  not solvent:
            QMessageBox.warning(self, "提示", "输入为空")
        else:
            #输入模型，返回预测值
            delt_g = delt_g_main(solute, solvent)
            output,  map = delt_g[0], delt_g[1]
            #获得分子二维结构图
            mol1 = Chem.MolFromSmiles(solute)
            mol2 = Chem.MolFromSmiles(solvent)

            photo1 = Draw.MolToImage(mol1)
            photo2 = Draw.MolToImage(mol2)

            # 转换为数据流
            byte_array1 = io.BytesIO()
            photo1.save(byte_array1, format='PNG')
            byte_array1.seek(0)

            byte_array2 = io.BytesIO()
            photo2.save(byte_array2, format='PNG')
            byte_array2.seek(0)

            q_img1 = QImage.fromData(byte_array1.read())
            pixmap1 = QPixmap.fromImage(q_img1)
            map_label1 = QLabel(self)
            name_label1 = QLabel(self)
            name_label1.setText('溶质分子的二维结构图：')
            name_label1.setFont(font)
            map_label1.setPixmap(pixmap1)

            q_img2 = QImage.fromData(byte_array2.read())
            pixmap2 = QPixmap.fromImage(q_img2)
            map_label2 = QLabel(self)
            name_label2 = QLabel(self)
            name_label2.setText('溶剂分子的二维结构图：')
            name_label2.setFont(font)


            map_label2.setPixmap(pixmap2)
            #返回结果弹窗
            result_label = QLabel(self)
            result_label.setText(('溶剂化自由能为:{0} kcal/mol').format(output.item()))
            result_label.setFont(font)
            #嵌套
            self.layout1.addWidget(name_label1, 0, 0)
            self.layout1.addWidget(name_label2, 5, 0)
            self.layout1.addWidget(map_label1, 1, 0, 3 ,3)
            self.layout1.addWidget(map_label2, 6, 0, 3, 3)
            self.layout1.addWidget(result_label, 9, 0)

            scroll_area.setWidget(self.frameg)
            # 嵌套
            self.layout4 = QVBoxLayout(self)
            self.layout4.addWidget(scroll_area)
            self.msg_box1.setLayout(self.layout4)
            self.msg_box1.show()

    def tox_21(self):
        #获取分子式
        molecule = self.lineEdit.text()
        if molecule:
            # 设置字体
            font = QFont()
            font.setPointSize(15)
            font.setBold(False)
            font.setFamily('宋体')

            font1 = QFont()
            font1.setPointSize(18)
            font1.setBold(True)
            font1.setFamily('宋体')
            # 创建滚动区域
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)  # 允许滚动区域自适应大小
            # 设置messagebox
            self.msg_box2 = QWidget()
            self.msg_box2.setWindowIcon(icon)
            self.msg_box2.resize(500, 500)
            self.msg_box2.setWindowTitle("result")
            self.framex = QFrame(self)
            self.layout3 = QVBoxLayout(self.framex)
            # 输入模型,返回预测值
            output, photo = tox_21_main(molecule)
            #获取分子二维结构图
            mol = Chem.MolFromSmiles(molecule)
            photo3 = Draw.MolToImage(mol)
            byte_array3 = io.BytesIO()
            photo3.save(byte_array3, format='PNG')
            byte_array3.seek(0)

            q_img3 = QImage.fromData(byte_array3.read())
            pixmap3 = QPixmap.fromImage(q_img3)
            #弹出结果

            map_label3 = QLabel(self)
            map_label3.setPixmap(pixmap3)
            map_label3.setAlignment(Qt.AlignHCenter)
            name_label = QLabel(self)
            name_label.setText('{}分子的二维结构图：'.format(molecule))
            name_label.setAlignment(Qt.AlignHCenter)
            name_label.setFont(font)
            self.layout3.addWidget(name_label)
            self.layout3.addWidget(map_label3)

            attn_label = QLabel(self)
            attn_label.setText('(0代表无该毒性，1代表有该毒性)')
            attn_label.setAlignment(Qt.AlignCenter)
            attn_label.setFont(font1)
            self.layout3.addWidget(attn_label)

            num = ['a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a11','a12']
            labels = ['NR-AR(雌激素受体激活与抑制活性):',
                      'NR-AR-LBD(雌激素受体亚型的配体结合结构域激活与抑制活性):',
                      'NR-AhR(芳香烃受体激活活性):',
                      'NR-Aromatase(芳香化酶抑制活性):',
                      'NR-ER(雌激素受体亚型激活活性):',
                      'NR-ER-LBD(雌激素受体亚型的配体结合结构域激活与抑制活性):',
                      'NR-PPAR-gamma(过氧化物酶体增殖物激活受体-gamma激活与抑制活性):',
                      'SR-ARE(抗氧化反应元件激活活性):',
                      'SR-ATAD5(ATAD5 核酸交联修复相关的ATP酶活性起动剂激活活性):',
                      'SR-HSE(热休克响应元件激活活性):',
                      'SR-MMP(基质金属蛋白酶激活与抑制活性):',
                      'SR-p53(肿瘤蛋白 p53 激活与抑制活性):']

            for i in range(12):
                num[i] = QLabel(self)
                dd = QLabel(self)
                ss = QLabel(self)
                msg = '{}{}'.format(labels[i],str(output[i]))
                num[i].setText(msg)
                num[i].setAlignment(Qt.AlignCenter)  # Qt.AlignRight)
                num[i].setFont(font)
                self.layout3.addWidget(num[i])
                #预测毒性基团
                if photo[i] != []:
                    byte_array = io.BytesIO()
                    photo[i].save(byte_array, format='PNG')
                    byte_array.seek(0)
                    q_img = QImage.fromData(byte_array.read())
                    pixmap = QPixmap.fromImage(q_img)
                    ss.setText('提供毒性的子结构为:')
                    ss.setAlignment(Qt.AlignHCenter)
                    dd.setPixmap(pixmap)
                    dd.setAlignment(Qt.AlignCenter)
                    self.layout3.addWidget(ss)
                    self.layout3.addWidget(dd)


            #设置布局
            scroll_area.setWidget(self.framex)
            # 嵌套
            self.layout4 = QVBoxLayout(self)
            self.layout4.addWidget(scroll_area)
            self.msg_box2.setLayout(self.layout4)
            self.msg_box2.show()
        else:
            QMessageBox.warning(self, "提示", "输入为空")

    def Batch_import(self):
        global content_pd
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        files = file_dialog.getOpenFileNames(self, "选择要导入的文件", '', 'CSV文件(*.csv);;TXT文件(*.txt)')
        font = QFont()
        font.setPointSize(12)
        font.setFamily('宋体')
        if files:
            for file_path in files[0]:
                file_ext = os.path.splitext(file_path)[1]
                if file_ext == ".csv":
                    content_pd = pd.read_csv(file_path,sep=';') # 读取CSV文件
                elif file_ext == ".txt":
                    content_pd = pd.read_csv(file_path, delimiter=";") # 读取文本文件

                content = content_pd.to_string(index=range(1, len(content_pd) + 1))
                self.plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
                self.plainTextEdit.setPlainText(content)
                self.plainTextEdit.setFont(font)

    def Batch_predict(self):
        column_names = content_pd.columns.tolist()
        if self.radioButton_2.isChecked():
            if 'smiles' in column_names:
                labels = ['NR-AR', 'NR-AR-LBD', 'NR-AhR', 'NR-Aromatase', 'NR-ER', 'NR-ER-LBD',
                          'NR-PPAR-gamma', 'SR-ARE', 'SR-ATAD5', 'SR-HSE', 'SR-MMP', 'SR-p53']
                for i in range(12):
                    content_pd[labels[i]] = None
                smiles_list = content_pd['smiles']

                self.worker_thread = ToxThread(smiles_list)
                self.worker_thread.update_progress.connect(self.update_progress_bar)
                self.worker_thread.result_ready.connect(self.handle_result)
                self.worker_thread.finished.connect(self.display_result)
                self.worker_thread.start()
            else:
                QMessageBox.warning(self, '警告', '文件中无可匹配列名:smiles')

        elif self.radioButton.isChecked():
            if 'SoluteSMILES' in column_names and 'SolventSMILES' in column_names:
                label = ['DeltaGsolv']
                solute = content_pd['SoluteSMILES']
                solvent = content_pd['SolventSMILES']
                content_pd[label] = None
                self.worker_thread = SolvThread(solute, solvent)
                self.worker_thread.update_progress.connect(self.update_progress_bar)
                self.worker_thread.result_ready.connect(self.handle_result)
                self.worker_thread.finished.connect(self.display_result)
                self.worker_thread.start()
            else:
                QMessageBox.warning(self, '警告', '文件中无可匹配列名:SoluteSMILES & SolventSMILES')

        else:
            QMessageBox.warning(self,'警告','请选择模型')
    def Batch_save(self):
        files = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV文件(*.csv);;TXT文件(*.txt)')
        if files[0]:
            file_path = files[0]
            content_pd.to_csv(file_path)
            QMessageBox.information(self,'提示','文件保存完毕')

    # 更新进度条
    def update_progress_bar(self, progress):
        self.progressBar.setValue(progress)
        if progress == '100':
            self.worker_thread.terminate()

    # 显示处理结果
    def display_result(self, result):
        QMessageBox.information(self, '提示', '进程已完成')

    # 处理子线程传递的结果
    def handle_result(self, processed_data):
        Vscrollbar = self.plainTextEdit.verticalScrollBar()
        Vscrollbar_pos = Vscrollbar.value()
        Hscrollbar = self.plainTextEdit.horizontalScrollBar()
        Hscrollbar_pos = Hscrollbar.value()

        if self.radioButton_2.isChecked():
            for i in range(12):
                content_pd.loc[processed_data[1]-1][i + 1] = processed_data[0][i]
            content = content_pd.to_string(index=range(1, len(content_pd) + 1))
            self.plainTextEdit.setPlainText(content)
        elif self.radioButton.isChecked():
            content_pd.loc[processed_data[1]-1][-1] = processed_data[0]
            content = content_pd.to_string(index=range(1, len(content_pd) + 1))
            self.plainTextEdit.setPlainText(content)
        Vscrollbar.setValue(Vscrollbar_pos)
        Hscrollbar.setValue(Hscrollbar_pos)

#子线程
class SolvThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    result_ready = pyqtSignal(list)

    def __init__(self, solute, solvent):
        super().__init__()
        self.solute = solute
        self.solvent = solvent

    def run(self):
        total = len(self.solute)
        for i in range(1 ,total + 1):
            # 模拟处理数据的操作，这里使用时间延迟来模拟处理耗时
            self.process_data(self.solute[i-1], self.solvent[i-1], i)

            # 发送更新进度信号
            progress = int(i / total * 100)
            self.update_progress.emit(progress)

        self.finished.emit("处理完成")

    def process_data(self, solute, solvent, index):
        # 实际的数据处理逻辑
        # 这里可以根据需要进行修改
        import time
        time.sleep(0.5)  # 模拟处理耗时
        delt_g = delt_g_main(solute, solvent)
        self.result_ready.emit([delt_g[0].item(),index])

class ToxThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    result_ready = pyqtSignal(list)

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        total = len(self.data)
        for i, item in enumerate(self.data, 1):
            # 模拟处理数据的操作，这里使用时间延迟来模拟处理耗时
            self.process_data(item, i)

            # 发送更新进度信号
            progress = int(i / total * 100)
            self.update_progress.emit(progress)

        self.finished.emit("处理完成")

    def process_data(self, item, index):
        # 实际的数据处理逻辑
        # 这里可以根据需要进行修改
        import time
        time.sleep(0.5)  # 模拟处理耗时
        output, photo = tox_21_main(item)
        self.result_ready.emit([output,index])

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    main_win = MainWin()
    main_win.show()
    sys.exit(app.exec_())