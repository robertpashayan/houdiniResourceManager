import hou
import imp
import os
from PySide2 import QtCore, QtGui, QtWidgets
from houdiniResourceManager.core import core as rmCore

imp.reload(rmCore)

class sequancerTagPlacer(QtWidgets.QDialog):
	def __init__(self, old_path, tag, parent=None):
		super(sequancerTagPlacer, self).__init__(parent)
		if parent:
			self.setWindowTitle(self.parent.windowTitle() + " : Sequance Tag Placer")
			self.setParent(parent,  QtCore.Qt.Window)
		else:
			self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
		self.old_path = old_path
		self.new_path = old_path
		self.tag = tag
		self.setFixedHeight(150)
		self.setMinimumWidth(800)
		self.init_ui()

	def init_ui(self):
		self.h2 = QtGui.QFont()
		self.h2.setPointSize(10)
		self.h2.setBold(True)
		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.path_label = QtWidgets.QLabel()
		self.path_label.setFont(self.h2)
		self.main_layout.addWidget(self.path_label)

		self.controls = QtWidgets.QWidget()
		self.controls.setFixedWidth(790)
		self.controls_layout = QtWidgets.QHBoxLayout()

		self.start_pos_label = QtWidgets.QLabel(" Indicate Start Position  ")
		self.start_pos_label.setFont(self.h2)
		self.start_pos_spiner = QtWidgets.QSpinBox()
		self.start_pos_spiner.setMaximum(len(self.old_path) - 1)
		self.start_pos_spiner.setMinimum(0)
		self.length_label = QtWidgets.QLabel(" Indicate length  ")
		self.length_label.setFont(self.h2)
		self.length_spiner = QtWidgets.QSpinBox()
		self.length_spiner.setMaximum(len(self.old_path))
		self.length_spiner.setMinimum(1)
		self.btn_validate = QtWidgets.QPushButton("Validate")
		self.btn_validate.setFixedHeight(60)
		self.controls_layout.addWidget(self.start_pos_label)
		self.controls_layout.addWidget(self.start_pos_spiner)
		self.controls_layout.addWidget(self.length_label)
		self.controls_layout.addWidget(self.length_spiner)
		self.controls_layout.addWidget(self.btn_validate)
		self.controls_layout.setContentsMargins(10, 0, 0, 0)
		self.controls.setLayout(self.controls_layout)

		self.main_layout.addWidget(self.path_label)
		self.main_layout.addWidget(self.controls)
		self.setLayout(self.main_layout)
