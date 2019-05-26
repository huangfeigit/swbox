#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import QTextEdit, QPushButton
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from trunk.defines.settings import *
from trunk.defines.const import GetSecond
from trunk.entity import CBaseEntity

import os

class CEntity(CBaseEntity):

    m_Idx = 1
    m_Code = "watchdog_update"
    m_Name = "看门狗自动更新"

    def __init__(self):
        super(CEntity, self).__init__()
        self.m_Observer = None
        self.InitPanel()

    def InitPanel(self):
        self.m_Button = QPushButton("启动", self)
        self.m_Button.clicked.connect(self.on_push_button)
        self.m_Button.setGeometry(0, 0, 60, WIDGET_HEIGHT)

        self.m_EditText = QTextEdit(self)
        iOffY = self.m_Button.geometry().y() + self.m_Button.geometry().height()
        self.m_EditText.setReadOnly(True)
        iGap = 100  #实际会有右侧和下方的进度条缓冲区
        self.m_EditText.setGeometry(0, iOffY, 900 - iGap, 800 - iOffY - iGap)
        self.m_EditText.setStyleSheet("background-color:black; color:white;")
        self.m_EditText.append("欢迎使用看门狗自动更新")

    def append_text(self, sText):
        self.m_EditText.append(sText)
        oScroll = self.m_EditText.verticalScrollBar()
        oScroll.setSliderPosition(oScroll.maximum());

    def on_push_button(self):
        sText = self.m_Button.text()
        if sText == "启动":
            self.start_watchdog()
        elif sText == "停止":
            self.stop_watchdog()

    def valid_start(self, sPath):
        if not os.path.exists(sPath):
            print("路径不存在 %s" % sPath)
            return 0
        return 1

    def start_watchdog(self):
        sPath = "D:"
        if not self.valid_start(sPath):
            return
        self.append_text("---- watchdog start ----")
        self.m_Observer = Observer()
        self.m_Observer.schedule(CFileEventHandler(self), sPath, True)
        self.m_Observer.start()
        self.m_Button.setText("停止")

    def stop_watchdog(self):
        self.append_text("---- watchdog stop ----")
        self.m_Observer.stop()
        self.m_Observer = None
        self.m_Button.setText("启动")

class CFileEventHandler(FileSystemEventHandler):

    def __init__(self, parent):
        super(CFileEventHandler, self).__init__()
        self.m_Parent = parent
        self._file_update_time = {}

    def on_modified(self, filename):
        if filename.is_directory:
            return
        print("filename", filename)
        filename = filename.src_path.split(":")[-1]
        if not filename.endswith(".py"):
            return
        iTime = GetSecond()
        if self._file_update_time.get(filename, 0) == iTime:  #一次修改，回调2次，奇怪，原因不明
            return
        self._file_update_time[filename] = iTime
        self.m_Parent.append_text(filename)
