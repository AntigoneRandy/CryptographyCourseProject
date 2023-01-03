from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton,  QComboBox, QTextBrowser, QFileDialog, QDialog, QLineEdit, QLabel
from PySide2.QtCore import Signal
from PySide2.QtCore import Qt
from pysm4 import encrypt_cbc, decrypt_cbc, encrypt_ecb, decrypt_ecb
import os, sys

default_iv = '111111111'
currentpath = sys.path[0]

class ChildWindow(QDialog):
    configSignal = Signal(list)

    def __init__(self, parent=None) -> None:
        super(ChildWindow, self).__init__()
        self.init_ui()
        self.type = type

    def init_ui(self):
        self.resize(630, 130)
        self.setWindowTitle("SM4 文件加解密")

        self.button_confirm = QPushButton('开始', self)
        self.button_confirm.move(180, 100)
        self.button_confirm.clicked.connect(self.send_confirm)

        self.button_cancel = QPushButton('取消', self)
        self.button_cancel.move(380, 100)
        self.button_cancel.clicked.connect(self.send_cancel)

        self.button_filepath = QPushButton('选择要处理的文件', self)
        self.button_filepath.move(10, 30)
        self.button_filepath.resize(140, 20)
        self.button_filepath.clicked.connect(self.do_getFilename)

        self.button_dirpath = QPushButton('选择处理结果保存路径', self)
        self.button_dirpath.move(10, 53)
        self.button_dirpath.resize(140, 20)
        self.button_dirpath.clicked.connect(self.do_getDirname)

        self.key_inputbox = QLineEdit(self)
        self.key_inputbox.move(155, 10)
        self.key_inputbox.resize(450, 20)
        self.key_inputbox_label = QLabel(self)
        self.key_inputbox_label.move(10, 12)
        self.key_inputbox_label.resize(140, 18)
        self.key_inputbox_label.setText('请输入密钥：')
        self.key_inputbox_label.setAlignment(Qt.AlignHCenter)
        
        self.mode_choose = QComboBox(self)
        self.mode_choose.addItems(['ECB', 'CBC', 'Classic'])
        self.mode_choose.move(220, 76)
        self.mode_choose.resize(100, 20)
        self.mode_choose_label = QLabel(self)
        self.mode_choose_label.move(160, 78)
        self.mode_choose_label.resize(50, 18)
        self.mode_choose_label.setText("加密模式")
        self.mode_choose_label.setAlignment(Qt.AlignHCenter)

        self.misapp_choose = QComboBox(self)
        self.misapp_choose.addItems(['classic', 'stealth'])
        self.misapp_choose.move(420, 76)
        self.misapp_choose.resize(100, 20)
        self.misapp_choose_label = QLabel(self)
        self.misapp_choose_label.move(360, 78)
        self.misapp_choose_label.resize(50, 18)
        self.misapp_choose_label.setText("填充模式")
        self.misapp_choose_label.setAlignment(Qt.AlignHCenter)

        self.show_filepath = QLabel(self)
        self.show_filepath.move(155, 30)
        self.show_filepath.resize(450, 18)
        self.show_dirpath = QLabel(self)
        self.show_dirpath.move(155, 53)
        self.show_dirpath.resize(450, 18)

        self.setting_label = QLabel(self)
        self.setting_label.move(10, 78)
        self.setting_label.resize(140, 18)
        self.setting_label.setText("加密高级设置：")
        self.setting_label.setAlignment(Qt.AlignHCenter)


    def do_getFilename(self):
        self.filepath, _ = QFileDialog.getOpenFileName(
            self,
            '选择文件',
            currentpath,
            ""
        )
        self.show_filepath.setText(self.filepath)

    def do_getDirname(self):
        self.dirpath, _ = QFileDialog.getSaveFileName(self, '选择位置')
        self.show_dirpath.setText(self.dirpath)

    def send_confirm(self):
        key = self.key_inputbox.text()
        mode = self.mode_choose.currentText()
        misapp_mode = self.misapp_choose.currentText()
        content = [self.filepath, self.dirpath, key, mode, misapp_mode]
        self.configSignal.emit(content)
        self.close()

    def send_cancel(self):
        content = [None]
        self.configSignal.emit(content)
        self.close()

class Stats():
    def __init__(self):
        self.window = QMainWindow()
        self.window.resize(500, 500)
        self.window.move(300, 310)
        self.window.setWindowTitle('SM4')

        self.toplabel = QLabel(self.window)
        self.toplabel.move(100, 10)
        self.toplabel.resize(300, 20)
        self.toplabel.setText("欢迎使用基于SM4的文件加密系统")
        self.toplabel.setAlignment(Qt.AlignHCenter)

        self.textbox = QTextBrowser(self.window)
        self.textbox.move(10,90)
        self.textbox.resize(480, 280)
        self.textbox.append("软件日志：\n")

        self.button_enc = QPushButton('文件加密', self.window)
        self.button_enc.move(100, 40)
        self.button_enc.clicked.connect(self.handle_button_enc)

        self.button_dec = QPushButton('文件解密',self.window)
        self.button_dec.move(300, 40)
        self.button_dec.clicked.connect(self.handle_button_dec)

        self.bottomlabel = QLabel(self.window)
        self.bottomlabel.move(10, 390)
        self.bottomlabel.resize(480, 100)
        self.bottomlabel.setText("软件特性：\n1.使用SM4的加密方法\n2.提供多种加密模式\n3.提供速度统计功能\nby:NMSL")


    def handle_button_enc(self):
        tmp_enc_window = ChildWindow(self)
        tmp_enc_window.configSignal.connect(self.do_enc)
        tmp_enc_window.exec_()

    def do_enc(self, connect):
        if connect[0] == None:
            return
        else:
            with open(connect[0], mode='rb') as f:
                content = f.read()
            if connect[3] == 'CBC':
                result_text, using_time = encrypt_cbc(content, connect[2], default_iv, connect[4])
            elif connect[3] == 'ECB':
                result_text, using_time = encrypt_ecb(content, connect[2], connect[4])
            else:
                result_text, using_time = encrypt_ecb(content, connect[2], connect[4])
            stats = os.stat(connect[0])
            size = stats.st_size
            speed = size / using_time
            f_result = open(connect[1], 'wb')
            f_result.write(result_text)
            f_result.close()
            self.textbox.append("使用模式%s加密文件%s，用时%4fms，速度： %4fbyte/ms\n"%(connect[3], connect[0], using_time, speed))
        

    def handle_button_dec(self):
        tmp_enc_window = ChildWindow(self)
        tmp_enc_window.configSignal.connect(self.do_dec)
        tmp_enc_window.exec_()

    def do_dec(self, connect):
        if connect[0] == None:
            return
        else:
            with open(connect[0], mode='rb') as f:
                content = f.read()
            if connect[3] == 'CBC':
                result_text, using_time = decrypt_cbc(content, connect[2], default_iv, connect[4])
            elif connect[3] == 'ECB':
                result_text, using_time = decrypt_ecb(content, connect[2], connect[4])
            else:
                result_text, using_time = decrypt_ecb(content, connect[2], connect[4])
            stats = os.stat(connect[0])
            size = stats.st_size
            speed = size / using_time
            f_result = open(connect[1], 'wb')
            f_result.write(result_text)
            f_result.close()
            self.textbox.append("使用模式%s解密文件%s，用时%4fms，速度： %4fbyte/ms\n"%(connect[3], connect[0], using_time, speed))

app = QApplication([])

stats = Stats()
stats.window.show()

app.exec_()