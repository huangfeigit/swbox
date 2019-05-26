#-*- coding:utf-8 -*-

def FailMessage(sText):
    from PyQt5.QtWidgets import QMessageBox
    QMessageBox.warning(None, "拒绝提示", sText)
