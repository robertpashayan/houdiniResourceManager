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
        self.setFixedHeight(55)
        self.layout = QtWidgets.QHBoxLayout()

        self.btn_scan = QtWidgets.QPushButton("Collect Nodes")
        self.btn_scan.setFixedSize(110, 54)
        self.btn_scan.clicked.connect(self.collect_nodes)
        self.layout.addWidget(self.btn_scan)

        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(18,0,0,0)
        
        self.containter_types_grp = QtWidgets.QGroupBox("Node Types")
        self.containter_types_grp.setContentsMargins(10,0,0,0)
        self.containter_types_grp.setFixedHeight(54)
        self.layout.addWidget(self.containter_types_grp)
        self.containter_types_grp_layout = QtWidgets.QHBoxLayout()
        self.containter_types_grp_layout.setAlignment(QtCore.Qt.AlignTop)
        self.containter_types_grp_layout.setContentsMargins(10,0,0,0)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.containter_type_checkboxes = []
        top_margin = 4
        for i,containter_type in enumerate(rmCore.container_types) :
            
            containter_type_widget = QtWidgets.QWidget()
            containter_type_widget.setContentsMargins(0,top_margin,0,0)
            containter_type_layout = QtWidgets.QHBoxLayout()
            containter_type_layout.setContentsMargins(0,top_margin,0,0)
            containter_type_label = QtWidgets.QLabel(containter_type.replace("_"," ").title())
            containter_type_label.setContentsMargins(1,top_margin,0,0)
            containter_type_checkbox = QtWidgets.QCheckBox()
            containter_type_checkbox.setContentsMargins(0,top_margin,0,0)
            containter_type_checkbox.setObjectName(containter_type)
            containter_type_layout.addWidget(containter_type_checkbox)
            containter_type_layout.addWidget(containter_type_label)
            containter_type_widget.setLayout(containter_type_layout)
            containter_type_layout.setAlignment(QtCore.Qt.AlignLeft)
            containter_type_checkbox.clicked.connect(self.activate_module)
            self.containter_types_grp_layout.addWidget(containter_type_widget)
            self.containter_type_checkboxes.append(containter_type_checkbox)

        self.containter_types_grp.setLayout(self.containter_types_grp_layout)
        self.setLayout(self.layout)

    def activate_module(self):
        rmCore.container_modules_activation_state = [(chkbox.checkState() == QtCore.Qt.CheckState.Checked) for chkbox in self.containter_type_checkboxes ]

    def collect_nodes(self):
        if self.parent:
            self.parent.elements = rmCore.collect()
            self.parent.refresh_qtable()
            self.parent.qtable.resizeColumnsToContents()
            