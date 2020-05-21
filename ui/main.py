import hou
import imp
import os
from PySide2 import QtCore, QtGui, QtWidgets
from houdiniResourceManager import resourceManagerCore as rmCore
from houdiniResourceManager.ui.modules import renamingToolsUI
from houdiniResourceManager.ui.modules import toolbarUI

imp.reload(rmCore)
imp.reload(renamingToolsUI)
imp.reload(toolbarUI)

"""
TODO:
Inspect option in table view, which will focus on the selected node in the node view
"""

class sequancerTagPlacer(QtWidgets.QDialog):
	def __init__(self, old_path, tag, parent=None):
		super(sequancerTagPlacer, self).__init__(parent)
		self.parent = parent
		self.setWindowTitle(self.parent.windowTitle() + " : Sequance Tag Placer")
		self.setParent(parent,  QtCore.Qt.Window)
		self.old_path = old_path
		self.new_path = old_path
		self.tag = tag
		self.setFixedHeight(150)
		self.setMinimumWidth(800)
		self.init_ui()
		
		

	def init_ui(self):
		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.path_label = QtWidgets.QLabel()
		self.path_label.setFont(self.parent.h2)
		self.main_layout.addWidget(self.path_label)

		self.controls = QtWidgets.QWidget()
		self.controls.setFixedWidth(790)
		self.controls_layout = QtWidgets.QHBoxLayout()

		self.start_pos_label = QtWidgets.QLabel(" Indicate Start Position  ")
		self.start_pos_label.setFont(self.parent.h2)
		self.start_pos_spiner = QtWidgets.QSpinBox()
		self.start_pos_spiner.setMaximum(len(self.old_path) - 1)
		self.start_pos_spiner.setMinimum(0)
		self.length_label = QtWidgets.QLabel(" Indicate length  ")
		self.length_label.setFont(self.parent.h2)
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
		self.refresh_qtable()

	def refresh_qtable(self):
		start = self.start_pos_spiner.value()
		length = self.length_spiner.value()
		self.new_path = self.old_path[0:start] + self.tag + self.old_path[start+length:]
		self.path_label.setText("    " + self.new_path)

	def closeEvent(self, event):
		self.parent.sequancerTagPlacerValue = self.new_path

class resourceManagerUI(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super(resourceManagerUI, self).__init__(parent)
		self.version = 'alpha v0.0'
		self.setWindowTitle('Houdini Node Resource Manager' + ' ' + self.version)
		self.width = 1279
		self.height = 677
		self.resize(self.width, self.height)
		self.title_font = QtGui.QFont("Calibri")
		self.title_font.setWeight(99)
		self.title_font.setPointSize(14)
		self.label_font = QtGui.QFont("Calibri")
		self.label_font.setWeight(80)
		self.label_font.setPointSize(10)
		self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
		self.elements = []
		self.sequancerTagPlacerValue = None
		self.init_ui()


	def init_ui(self):
		# Main Sections
		self.h2 = QtGui.QFont()
		self.h2.setPointSize(11)
		self.h2.setBold(True)

		self.main_layout = QtWidgets.QVBoxLayout()

		self.toolbar = toolbarUI.toolbar_UI(self)

		self.body_widget = QtWidgets.QWidget()

		self.progress_bar = QtWidgets.QProgressBar()
		self.progress_bar.setMaximum(100)
		self.progress_bar.setMinimum(0)
		self.progress_bar.setValue(50)

		self.main_layout.addWidget(self.toolbar)
		self.main_layout.addWidget(self.body_widget)
		self.main_layout.addWidget(self.progress_bar)

		self.setLayout(self.main_layout)

		self.init_ui_body()
		css_file = os.path.join((os.path.dirname(__file__)), 'ui.css')
		css_content = open(css_file,"r")
		css_template = str(css_content.read())
		css_content.close()
		self.setStyleSheet(css_template)

	def init_ui_body(self):
		self.body_layout = QtWidgets.QHBoxLayout()
		self.content_layout = QtWidgets.QVBoxLayout()

		self.content_panel = QtWidgets.QWidget()
		# self.side_panel = QtWidgets.QWidget()
		# self.side_panel.setFixedWidth(250)

		self.body_layout.addWidget(self.content_panel)
		# self.body_layout.addWidget(self.side_panel)

		self.qtable = QtWidgets.QTableWidget()
		self.qtable.setShowGrid(False)
		self.qtable.verticalHeader().setVisible(False)
		self.qtableColumns = ['Node Path', 'Resource FilePath']
		self.qtable.setColumnCount(len(self.qtableColumns))
		self.qtable.setHorizontalHeaderLabels(self.qtableColumns)
		self.qtable.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
		self.header = self.qtable.horizontalHeader()

		self.header.setStyleSheet("""
		QHeaderView::section
		{
			background-color: rgb(38, 37, 42); color: rgb(196,196,196);
		}
		QHeaderView::section:pressed
		{
			background-color: rgb(43, 42, 47);
			color: white;
		}
		""")
		self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
		self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		self.content_layout.addWidget(self.qtable)

		self.renaming_tools = renamingToolsUI.renamingTools_UI(self)
		self.content_layout.addWidget(self.renaming_tools)

		self.content_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.body_layout.setAlignment(QtCore.Qt.AlignLeft)

		self.content_panel.setLayout(self.content_layout)
		self.body_widget.setLayout(self.body_layout)

	def refresh_qtable(self):
		self.qtable.setRowCount(len(self.elements))
		for row in range(len(self.elements)):
			file_path = rmCore.get_file_path(self.elements[row])
			col_elements = [(" " + self.elements[row].path()+" "),( " "+ file_path +" ")]
			for column in range(len(self.qtableColumns)):
				item = QtWidgets.QLabel(col_elements[column])
				self.qtable.setCellWidget(row, column, item)
	
	def qtable_get_selected(self):
		return (self.qtable.selectionModel().selectedRows())

	def init_sequancerTagPlacer(self, old_path, sequance_tag):
		self.sequancerTagPlacerUI = sequancerTagPlacer(old_path,sequance_tag, parent=self)
		self.sequancerTagPlacerUI.show()

	def closeEvent(self, event):
		if self.sequancerTagPlacerUI:
			self.sequancerTagPlacerUI.close()
		print(self.windowTitle() + " is closing")