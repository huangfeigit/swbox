#-*- coding:utf-8 -*-
#核心代码

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QSplitter, QStackedWidget, QDesktopWidget
from PyQt5.QtGui import QIcon

class CMainWindows(QWidget):

    def __init__(self):
        super(CMainWindows, self).__init__()
        self.InitView()

    def InitView(self):
        from trunk import entity

        self.setFixedSize(960, 800)
        self.SetCenter()
        self.setFixedSize(self.width(), self.height());
        self.setWindowTitle("神武3工具箱")
        self.setWindowIcon(QIcon("trunk/images/title_red.png"))

        self.m_MainLayout = QHBoxLayout(self)  # 新建一个水平布局作为本窗体的主布局
        self.m_MainLayout.setSpacing(10)  # 设置主布局内边距以及控件间距为10px

        self.m_ComBoxLayout = QVBoxLayout()  # 新建垂直子布局用于放置按键
        self.m_ComBoxLayout.setContentsMargins(10, 10, 10, 10)  # 设置此子布局和内部控件的间距为10px

        oLabel = QLabel(self)
        oLabel.setText(u"当前操作：")
        oLabel.setFixedHeight(20)
        self.m_ComBoxLayout.addWidget(oLabel)

        self.m_ComBox = QComboBox(self)

        for oEntry in entity.get_all_eneity():
            self.m_ComBox.addItem(oEntry.m_Name)
        self.m_ComBox.currentIndexChanged.connect(self.OnComBoxChange)
        self.m_ComBox.setFixedWidth(self.m_ComBox.width() + 10)

        self.m_ComBoxLayout.addWidget(self.m_ComBox)

        oSplitter = QSplitter(self)  # 占位符
        self.m_ComBoxLayout.addWidget(oSplitter)

        self.m_StackedWidget = QStackedWidget(self)
        for oEntry in entity.get_all_eneity():
            self.m_StackedWidget.addWidget(oEntry)

        self.m_MainLayout.addLayout(self.m_ComBoxLayout)  # 将子布局加入主布局
        self.m_MainLayout.addWidget(self.m_StackedWidget)

    def OnComBoxChange(self):
        self.m_StackedWidget.setCurrentIndex(self.m_ComBox.currentIndex())

    def SetSize(self, iHeight, iWidth):
        self.resize(iHeight, iWidth)

    def SetCenter(self):  # 主窗口居中显示函数
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
