import imp
import os
import hou
from PySide2 import QtCore,QtGui, QtWidgets
from houdiniResourceManager import resourceManagerCore as rmCore

imp.reload(rmCore)

class toolbar_UI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(toolbar_UI,self).__init__(parent)
        self.parent = parent
        self.setFixedHeight(50)
        self.layout = QtWidgets.QHBoxLayout()

        self.btn_scan = QtWidgets.QPushButton("Scan")
        self.btn_scan.setFixedSize(80, 48)
        self.btn_scan.clicked.connect(self.scan_scene)
        self.layout.addWidget(self.btn_scan)


        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.setContentsMargins(18,1,0,0)
        self.setLayout(self.layout)

    def scan_scene(self):
        if self.parent:
		    self.parent.elements = rmCore.collect()
		    self.parent.refresh_qtable()