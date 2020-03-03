import imp
import os
import hou
from PySide2 import QtCore, QtGui, QtWidgets
from houdiniResourceManager import resourceManagerCore as rmCore

imp.reload(rmCore)

class renamingTools_UI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(renamingTools_UI, self).__init__(parent)
        self.parent = parent
        self.setFixedHeight(150)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.replaceUI = QtWidgets.QWidget()
        self.replaceUI_layout = QtWidgets.QVBoxLayout()
        self.replaceUI_layout.setContentsMargins(0, 0, 0, 0)
        self.replaceUI.setLayout(self.replaceUI_layout)

        self.replaceUI_head = QtWidgets.QWidget()
        self.replaceUI_headL = QtWidgets.QCheckBox()
        self.replaceUI_headCh = QtWidgets.QLabel("Replace")
        self.replaceUI_headCh.setFont(self.parent.h2)
        self.replaceUI_head_Layout = QtWidgets.QHBoxLayout()
        self.replaceUI_head_Layout.setContentsMargins(0, 0, 0, 0)
        self.replaceUI_head_Layout.setAlignment(QtCore.Qt.AlignLeft)
        self.replaceUI_head_Layout.addWidget(self.replaceUI_headL)
        self.replaceUI_head_Layout.addWidget(self.replaceUI_headCh)
        self.replaceUI_head.setLayout(self.replaceUI_head_Layout)

        self.replaceUI_editFrom = QtWidgets.QWidget()
        self.replaceUI_editFrom_Layout = QtWidgets.QHBoxLayout()
        self.replaceUI_editFrom_Layout.setContentsMargins(5, 0, 0, 0)
        self.replaceUI_editFrom.setLayout(self.replaceUI_editFrom_Layout)
        self.replaceUI_editFromL = QtWidgets.QLabel("From")
        self.replaceUI_editFromE = QtWidgets.QLineEdit()
        self.replaceUI_editFrom_Layout.addWidget(self.replaceUI_editFromL)
        self.replaceUI_editFrom_Layout.addWidget(self.replaceUI_editFromE)

        self.replaceUI_editTo = QtWidgets.QWidget()
        self.replaceUI_editTo_Layout = QtWidgets.QHBoxLayout()
        self.replaceUI_editTo_Layout.setContentsMargins(20, 0, 0, 0)
        self.replaceUI_editTo.setLayout(self.replaceUI_editTo_Layout)
        self.replaceUI_editToL = QtWidgets.QLabel("To")
        self.replaceUI_editToE = QtWidgets.QLineEdit()
        self.replaceUI_editTo_Layout.addWidget(self.replaceUI_editToL)
        self.replaceUI_editTo_Layout.addWidget(self.replaceUI_editToE)

        self.replaceUI_layout.addWidget(self.replaceUI_head)
        self.replaceUI_layout.addWidget(self.replaceUI_editFrom)
        self.replaceUI_layout.addWidget(self.replaceUI_editTo)
        self.layout.addWidget(self.replaceUI)

        self.addUI = QtWidgets.QWidget()
        self.addUI_layout = QtWidgets.QVBoxLayout()
        self.addUI_layout.setContentsMargins(25, 0, 0, 0)
        self.addUI.setLayout(self.addUI_layout)

        self.addUI_head = QtWidgets.QWidget()
        self.addUI_headL = QtWidgets.QCheckBox()
        self.addUI_headCh = QtWidgets.QLabel("Add")
        self.addUI_headCh.setFont(self.parent.h2)
        self.addUI_head_Layout = QtWidgets.QHBoxLayout()
        self.addUI_head_Layout.setContentsMargins(0, 0, 0, 0)
        self.addUI_head_Layout.setAlignment(QtCore.Qt.AlignLeft)
        self.addUI_head_Layout.addWidget(self.addUI_headL)
        self.addUI_head_Layout.addWidget(self.addUI_headCh)
        self.addUI_head.setLayout(self.addUI_head_Layout)

        self.addUI_prefix = QtWidgets.QWidget()
        self.addUI_prefix_Layout = QtWidgets.QHBoxLayout()
        self.addUI_prefix_Layout.setContentsMargins(20, 0, 0, 0)
        self.addUI_prefix.setLayout(self.addUI_prefix_Layout)
        self.addUI_prefCh = QtWidgets.QCheckBox()
        self.addUI_prefL = QtWidgets.QLabel("Prefix")
        self.addUI_prefE = QtWidgets.QLineEdit()
        self.addUI_prefix_Layout.addWidget(self.addUI_prefCh)
        self.addUI_prefix_Layout.addWidget(self.addUI_prefL)
        self.addUI_prefix_Layout.addWidget(self.addUI_prefE)

        self.addUI_suffix = QtWidgets.QWidget()
        self.addUI_suffix_Layout = QtWidgets.QHBoxLayout()
        self.addUI_suffix_Layout.setContentsMargins(20, 0, 0, 0)
        self.addUI_suffix.setLayout(self.addUI_suffix_Layout)
        self.addUI_prefCh = QtWidgets.QCheckBox()
        self.addUI_prefL = QtWidgets.QLabel("Suffix")
        self.addUI_prefE = QtWidgets.QLineEdit()
        self.addUI_suffix_Layout.addWidget(self.addUI_prefCh)
        self.addUI_suffix_Layout.addWidget(self.addUI_prefL)
        self.addUI_suffix_Layout.addWidget(self.addUI_prefE)

        self.addUI_enum = QtWidgets.QWidget()
        self.addUI_enum_Layout = QtWidgets.QHBoxLayout()
        self.addUI_enum_Layout.setContentsMargins(20, 0, 0, 0)
        self.addUI_enum.setLayout(self.addUI_enum_Layout)
        self.addUI_enumCh = QtWidgets.QCheckBox()
        self.addUI_enumL = QtWidgets.QLabel("Enumerate")
        self.addUI_enumFL = QtWidgets.QLabel(" from")
        self.addUI_enumF = QtWidgets.QSpinBox()
        self.addUI_enumF.setMaximum(9999)
        self.addUI_enumTL = QtWidgets.QLabel(" to")
        self.addUI_enumT = QtWidgets.QSpinBox()
        self.addUI_enumT.setMaximum(9999)
        self.addUI_enumDL = QtWidgets.QLabel(" digits")
        self.addUI_enumD = QtWidgets.QSpinBox()
        self.addUI_enumD.setMaximum(9999)
        self.addUI_enum_Layout.addWidget(self.addUI_enumCh)
        self.addUI_enum_Layout.addWidget(self.addUI_enumL)
        self.addUI_enum_Layout.addWidget(self.addUI_enumFL)
        self.addUI_enum_Layout.addWidget(self.addUI_enumF)
        self.addUI_enum_Layout.addWidget(self.addUI_enumTL)
        self.addUI_enum_Layout.addWidget(self.addUI_enumT)
        self.addUI_enum_Layout.addWidget(self.addUI_enumDL)
        self.addUI_enum_Layout.addWidget(self.addUI_enumD)

        self.addUI_layout.addWidget(self.addUI_head)
        self.addUI_layout.addWidget(self.addUI_prefix)
        self.addUI_layout.addWidget(self.addUI_suffix)
        self.addUI_layout.addWidget(self.addUI_enum)
        self.layout.addWidget(self.addUI)

        self.ctrlsUI = QtWidgets.QWidget()
        self.ctrlsUI_layout = QtWidgets.QHBoxLayout()
        self.ctrlsUI_layout.setContentsMargins(20, 0, 0, 0)
        self.ctrlsUI.setLayout(self.ctrlsUI_layout)
        
        self.ctrlsUI_oprtions = QtWidgets.QWidget()
        self.ctrlsUI_oprtions_layout = QtWidgets.QVBoxLayout()
        self.ctrlsUI_oprtions_layout.setContentsMargins(0, 0, 0, 0)
        self.ctrlsUI_oprtions.setLayout(self.ctrlsUI_oprtions_layout)
        
        self.ctrlsUI_oprtions_file_management = QtWidgets.QComboBox()
        self.ctrlsUI_oprtions_file_management_options = ['Rename Files','Make Copies']
        self.ctrlsUI_oprtions_file_management.addItems(self.ctrlsUI_oprtions_file_management_options)
        self.ctrlsUI_oprtions_layout.addWidget(self.ctrlsUI_oprtions_file_management)

        self.ctrlsUI_oprtions_resource_affect = QtWidgets.QComboBox()
        self.ctrlsUI_oprtions_resource_affect_options = ['Rename Files & Input','Rename Input']
        self.ctrlsUI_oprtions_resource_affect.addItems(self.ctrlsUI_oprtions_resource_affect_options)
        self.ctrlsUI_oprtions_layout.addWidget(self.ctrlsUI_oprtions_resource_affect)

        self.ctrlsUI_btn_apply = QtWidgets.QPushButton("Apply")
        self.ctrlsUI_btn_apply.setFixedHeight(60)
        self.ctrlsUI_oprtions_layout.addWidget(self.ctrlsUI_btn_apply)

        self.ctrlsUI_layout.addWidget(self.ctrlsUI_oprtions)

        
        self.replaceUI_head_Layout = QtWidgets.QVBoxLayout()
        self.addUI_enum_Layout.setContentsMargins(20, 0, 0, 0)

    
        self.layout.addWidget(self.ctrlsUI)


        self.setLayout(self.layout)