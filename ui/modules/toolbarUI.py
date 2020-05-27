import imp
import os
import hou
from PySide2 import QtCore,QtGui, QtWidgets
from houdiniResourceManager.core import core as rmCore
from houdiniResourceManager.ui import custom_widgets

imp.reload(rmCore)
imp.reload(custom_widgets)

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
        self.layout.setContentsMargins(0,0,0,0)
        
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
        for node_type in rmCore.node_type_data:
            
            containter_type_widget = QtWidgets.QWidget()
            containter_type_widget.setContentsMargins(0,top_margin,0,0)
            containter_type_layout = QtWidgets.QHBoxLayout()
            containter_type_layout.setContentsMargins(0,top_margin,0,0)
            containter_type_label = QtWidgets.QLabel(node_type.replace("_"," ").title())
            containter_type_label.setContentsMargins(1,top_margin,0,0)
            containter_type_label.setFont(self.parent.h2)
            containter_type_checkbox = custom_widgets.CheckBox(data=node_type)
            containter_type_checkbox.setContentsMargins(0,top_margin,0,0)
            containter_type_checkbox.setObjectName(node_type)
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
        self.parent.node_types_to_collect = [chkbox.data for chkbox in self.containter_type_checkboxes if (chkbox.checkState() == QtCore.Qt.CheckState.Checked)]

    def collect_nodes(self):
        if self.parent:
            self.parent.elements = rmCore.collect(self.parent.node_types_to_collect)
            self.parent.refresh_qtable()
            self.parent.qtable.resizeColumnsToContents()
            