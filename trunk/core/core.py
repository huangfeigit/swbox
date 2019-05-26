#-*- coding:utf-8 -*-
#核心代码
from PyQt5.QtWidgets import QApplication

import sys

def run_swbox():
    from trunk.core import gui
    from trunk import entity
    app = QApplication(sys.argv)
    entity.init_entity()
    swbox = gui.CMainWindows()
    swbox.show()
    sys.exit(app.exec_())
