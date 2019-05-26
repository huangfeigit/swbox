#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import QPushButton
from trunk.entity import CBaseEntity

class CEntity(CBaseEntity):

    m_Idx = 2
    m_Code = "middle_merge"
    m_Name = u"Middle代码合并"

    def __init__(self):
        super(CEntity, self).__init__()
        self.InitPanel()

    def InitPanel(self):
        QPushButton("middle_merge", self)
