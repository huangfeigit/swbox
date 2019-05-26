#-*- coding:utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor

if not "g_EntityList" in globals():
    g_EntityList = {}

def init_entity():
    from . import middle_merge
    from . import codeline_count
    from . import watchdog_update

    g_EntityList["middle_merge"] = middle_merge.CEntity()
    g_EntityList["codeline_count"] = codeline_count.CEntity()
    g_EntityList["watchdog_update"] = watchdog_update.CEntity()

def get_entity(sType):
    global g_EntityList
    return g_EntityList.get(sType, None)

def get_entity_by_idx(idx):
    global g_EntityList
    for oEntity in g_EntityList.values():
        if oEntity.m_Idx == idx:
            return oEntity
    return None

def get_all_eneity():
    global g_EntityList
    lstEntity = list(g_EntityList.values())
    lstEntity.sort(key = lambda x: x.m_Idx)
    return lstEntity

class CBaseEntity(QWidget):

    def __init__(self):
        super(CBaseEntity, self).__init__()
        self.setFixedSize(800, 700)
        oWidget = QWidget(self)
        oWidget.setFixedSize(self.width(), self.height())
        oColor = QColor(255, 255, 255)
        oWidget.setStyleSheet("QWidget { background-color: %s }" % oColor.name())

    def Hide(self):
        self.hide()

    def Show(self):
        self.show()

