from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton,  QComboBox, QTextBrowser, QFileDialog, QDialog, QLineEdit, QLabel
from PySide2.QtCore import Signal
from pysm4 import encrypt_cbc, decrypt_cbc, encrypt, decrypt, encrypt_ecb, decrypt_ecb

default_iv = '111111111'

class ChildWindow(QDialog):
    configSignal = Signal(list)

    def __init__(self, parent=None) -> None:
        super(ChildWindow, self).__init__()
        self.init_ui()
        self.type = type

    def init_ui(self):
        self.resize(730, 100)
        self.button_confirm = QPushButton('确定', self)
        self.button_confirm.move(200, 70)
        self.button_confirm.clicked.connect(self.send_confirm)

        self.button_cancel = QPushButton('取消', self)
        self.button_cancel.move(430, 70)
        self.button_cancel.clicked.connect(self.send_cancel)

        self.button_filepath = QPushButton('选择文件', self)
        self.button_filepath.move(620, 10)
        self.button_filepath.clicked.connect(self.do_getFilename)

        self.button_dirpath = QPushButton('选择路径', self)
        self.button_dirpath.move(620, 30)
        self.button_dirpath.clicked.connect(self.do_getDirname)

        self.key_inputbox = QLineEdit(self)
        self.key_inputbox.move(80, 50)
        self.key_inputbox.resize(530, 20)
        self.key_inputbox_label = QLabel(self)
        self.key_inputbox_label.move(10, 50)
        self.key_inputbox_label.resize(70, 18)
        self.key_inputbox_label.setText('输入密钥：')
        
        self.mode_choose = QComboBox(self)
        self.mode_choose.addItems(['ECB', 'CBC', 'Classic'])
        self.mode_choose.move(620, 50)
        self.mode_choose.resize(100, 20)

        self.show_filepath = QLabel(self)
        self.show_filepath.move(10, 10)
        self.show_filepath.resize(600, 18)
        self.show_dirpath = QLabel(self)
        self.show_dirpath.move(10, 30)
        self.show_dirpath.resize(600, 18)


    def do_getFilename(self):
        self.filepath, _ = QFileDialog.getOpenFileName(
            self,
            '选择文件',
            r"C:\\Users\\13442\\Desktop\\course in WHU\\crypto\\pysm4",
            ""
        )
        self.show_filepath.setText(self.filepath)

    def do_getDirname(self):
        self.dirpath, _ = QFileDialog.getSaveFileName(self, '选择位置')
        self.show_dirpath.setText(self.dirpath)

    def send_confirm(self):
        key = self.key_inputbox.text()
        mode = self.mode_choose.currentText()
        content = [self.filepath, self.dirpath, key, mode]
        self.configSignal.emit(content)
        self.close()

    def send_cancel(self):
        content = [None]
        self.configSignal.emit(content)
        self.close()

class Stats():
    def __init__(self):
        self.window = QMainWindow()
        self.window.resize(500, 400)
        self.window.move(300, 310)
        self.window.setWindowTitle('SM4')

        self.textbox = QTextBrowser(self.window)
        self.textbox.move(10,110)
        self.textbox.resize(480, 280)

        self.button_enc = QPushButton('加密', self.window)
        self.button_enc.move(300, 40)
        self.button_enc.clicked.connect(self.handle_button_enc)

        self.button_dec = QPushButton('解密',self.window)
        self.button_dec.move(100, 40)
        self.button_dec.clicked.connect(self.handle_button_dec)

        # self.button.clicked.connect(self.handleCalc)

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
                result_text, using_time = encrypt_cbc(content, connect[2], default_iv)
            elif connect[3] == 'ECB':
                result_text, using_time = encrypt_ecb(content, connect[2])
            else:
                # result_text, using_time = encrypt(content, connect[2])
                # print(using_time)
                result_text, using_time = encrypt_ecb(content, connect[2])
            f_result = open(connect[1], 'wb')
            f_result.write(result_text)
            f_result.close()
            self.textbox.append('Encode file with mode' + connect[3] + ', using ' + str(using_time) + 'ms' + '\n')
        

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
                result_text, using_time = decrypt_cbc(content, connect[2], default_iv)
            elif connect[3] == 'ECB':
                result_text, using_time = decrypt_ecb(content, connect[2])
            else:
                result_text, using_time = decrypt_ecb(content, connect[2])
            f_result = open(connect[1], 'wb')
            f_result.write(result_text)
            f_result.close()
            self.textbox.append('Decode file with mode' + connect[3] + ', using ' + str(using_time) + 'ms' + '\n')

app = QApplication([])

stats = Stats()
stats.window.show()

app.exec_()