# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QProgressBar, QFileDialog

from trunk.entity import CBaseEntity
from trunk.defines.settings import *
from trunk.utils import FailMessage

import os

class CEntity(CBaseEntity):

    m_Idx = 1
    m_Code = "codeline_count"
    m_Name = "代码行数统计"

    def __init__(self):
        super(CEntity, self).__init__()
        self.m_Counter = CCounter(self)
        self.init()

    def init(self):
        iOffX = 20
        iOffY = 20
        self.m_PathLineEdit = QLineEdit(self)
        self.m_PathLineEdit.setDisabled(True)
        self.m_PathLineEdit.setGeometry(iOffX, iOffY, 500, WIDGET_HEIGHT)

        self.m_FileButton = QPushButton("浏览", self)
        self.m_FileButton.clicked.connect(self.on_push_file_button)
        iOffX, iOffY = self.GetTopRightPos(self.m_PathLineEdit)
        self.m_FileButton.setGeometry(iOffX + S_SPACE, iOffY, 60, WIDGET_HEIGHT)

        self.m_StartButton = QPushButton("开始", self)
        self.m_StartButton.clicked.connect(self.on_push_start_button)
        iOffX, iOffY = self.GetTopRightPos(self.m_FileButton)
        self.m_StartButton.setGeometry(iOffX + M_SPACE, iOffY, 60, WIDGET_HEIGHT)

        self.m_ResultLabel = QLabel("结果：", self)
        iOffX, iOffY = self.GetButtomLeftPos(self.m_PathLineEdit)
        self.m_ResultLabel.setGeometry(iOffX, iOffY + V_INTERVAL, 60, WIDGET_HEIGHT)

        self.m_ProgressLabel = QLabel("进度：", self)
        iOffX, iOffY = self.GetButtomLeftPos(self.m_ResultLabel)
        self.m_ProgressLabel.setGeometry(iOffX, iOffY + V_INTERVAL, 60, WIDGET_HEIGHT)
        self.m_ProgressLabel.hide()

        self.m_ProgressBar = QProgressBar(self)
        iOffX, iOffY = self.GetTopRightPos(self.m_ProgressLabel)
        self.m_ProgressBar.setGeometry(iOffX + S_SPACE, iOffY, 300, WIDGET_HEIGHT)
        self.m_ProgressBar.hide()

    def GetTopRightPos(self, oWidget):
        oGeometry = oWidget.geometry()
        iOffX = oGeometry.x() + oGeometry.width()
        iOffY = oGeometry.y()
        return iOffX, iOffY

    def GetButtomLeftPos(self, oWidget):
        oGeometry = oWidget.geometry()
        iOffX = oGeometry.x()
        iOffY = oGeometry.y() + oGeometry.height()
        return iOffX, iOffY

    def on_push_file_button(self):
        filename = QFileDialog.getExistingDirectory(self, '选择需要统计的目录', '')
        self.m_PathLineEdit.setText(filename)

    def on_push_start_button(self):
        sDir = self.m_PathLineEdit.text()
        if not sDir:
            FailMessage("请选择扫描目录")
            return
        if not os.path.exists(sDir):
            FailMessage("目录不存在")
            return
        iTotalLines = self.m_Counter.get_count_lines(sDir)
        self.m_ResultLabel.setText("结果：%s" % iTotalLines)

class CCounter(object):

    def __init__(self, parent):
        self.m_UI = parent
        self.m_FileList = {}

    def fileter_file(self, sPath):
        for root, dirs, filenames in os.walk(sPath):
            for filename in filenames:
                filetype = filename.split(".")[-1]
                if filetype == "py":
                    sTruePath = os.path.join(root, filename)
                    self.m_FileList[sTruePath] = 1
            for ddir in dirs:
                self.fileter_file(os.path.join(root, ddir))

    def count_file(self, filename):
        cnt = 0
        for sLine in open(filename, "rb").readlines():
            sLine = sLine.strip()
            if not sLine:
                continue
            cnt += 1
        return cnt

    def count_lines(self):
        iTotalLines = 0
        for filename in self.m_FileList.keys():
            iTotalLines += self.count_file(filename)
        return iTotalLines

    def get_count_lines(self, sPath):
        self.m_FileList = {}
        self.fileter_file(sPath)
        return self.count_lines()
