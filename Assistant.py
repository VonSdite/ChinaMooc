# -*- coding: utf-8 -*-
# __Author__: Sdite
# __Email__ : a122691411@gmail.com

import win32com.client as win32
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt

exam_bank = 'TCM_Exam_Bank.docx'

class Assistant(object):

    def __init__(self, exam_bank):
        super(Assistant, self).__init__()
        self.exam_bank = exam_bank

    def help(self):
        self.word = win32.gencache.EnsureDispatch('word.Application')
        self.word.Documents.Open(os.getcwd() + '/' + self.exam_bank)
        self.word.Visible = True
        self.seletion = self.word.Selection

        return self.seletion

    def find(self, text):
        self.seletion.SetRange(0, 0)
        self.seletion.Find.Execute(FindText=text, Forward=True)

    def delete_wrong_answer(self):
        self.selection.SetRange(0, 0)
        char_set1 = ['D', 'C', 'B', 'A']
        char_set2 = ['B', 'A']
        find = self.selection.Find

        while find.Execute(FindText='正确答案', Forward=True):
            self.selection.MoveUp(Count=2)
            self.selection.MoveStart(Unit=5)
            self.selection.MoveEnd(Unit=5)
            text_tmp = self.selection.Text
            if 'D' not in text_tmp:
                char_set = char_set2
            else:
                char_set = char_set1
            self.selection.MoveStart(Unit=5)
            self.selection.MoveEnd(Unit=5)
            text = self.selection.Text
            flag = False
            self.selection.SetRange(self.selection.End, self.selection.End)
            for c in char_set:
                if c not in text:
                    if find.Execute(FindText=c, Forward=False):
                        self.selection.MoveEnd(Unit=5)
                        self.selection.Delete()
                        flag = True

            if flag:
                find.Execute(FindText='正确答案', Forward=True)
                self.selection.SetRange(self.selection.End, self.selection.End)

    def delete_wrong_answer(self):
        self.seletion.SetRange(0, 0)
        char_set = ['D', 'C', 'B', 'A']
        find = self.selection.Find

        find.Execute(FindText='正确答案', Forward=True)
        self.selection.MoveEnd(Unit=5)
        text = self.selection.Text
        self.selection.SetRange(self.selection.End, self.selection.End)
        for c in char_set:
            if c not in text:
                find.Execute(FindText=c, Forward=False)
                self.selection.MoveEnd(Unit=5)
                self.selection.Delete()

    def exit(self):
        self.word.Application.Quit()


class UI(QMainWindow):

    def __init__(self, helper):
        super(UI, self).__init__()
        self.helper = helper
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)
        self.init_ui()
        self.resize(350, 50)

    def init_ui(self):
        self.setWindowTitle('word文档查找助手')
        self.mainWidget = QWidget()             # 主窗体控件
        self.mainLayout = QGridLayout()         # 主窗体layout

        exit = QPushButton('退出程序', self)
        exit.clicked.connect(self.close)

        self.mainLayout.addWidget(exit, 1, 1)

        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()

    def on_clipboard_change(self):
        text = self.clipboard.text()
        # print(text)
        helper.find(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, QCloseEvent):
        helper.exit()
        QCloseEvent.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 程序主体
    helper = Assistant(exam_bank)
    helper.help()

    ui = UI(helper)
    sys.exit(app.exec_())
