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

class CheckBox(QtWidgets.QCheckBox):
	def __init__(self, data=None):
		super(CheckBox, self).__init__()
		self.data = data

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
		self.setWindowTitle('Houdini Resource Manager' + ' ' + self.version)
		self.setMinimumSize(1279, 850)
		self.title_font = QtGui.QFont("Calibri")
		self.title_font.setWeight(99)
		self.title_font.setPointSize(14)
		self.label_font = QtGui.QFont("Calibri")
		self.label_font.setWeight(80)
		self.label_font.setPointSize(10)
		self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
		self.elements = []
		self.sequancerTagPlacerValue = None
		self.sequancerTagPlacerUI = None
		self.init_ui()
		self.init_signals()


	def init_ui(self):
		# Main Sections
		self.h2 = QtGui.QFont()
		self.h2.setPointSize(10)
		self.h2.setBold(True)

		self.main_layout = QtWidgets.QVBoxLayout()
		self.toolbar = toolbarUI.toolbar_UI(self)

		self.body_widget = QtWidgets.QWidget()

		self.status_grp = QtWidgets.QGroupBox("Status")
		self.status_message = QtWidgets.QLabel()
		self.status_message.setMinimumHeight(50)
		self.status_grp_layout = QtWidgets.QVBoxLayout()
		self.status_grp_layout.addWidget(self.status_message)
		self.status_grp.setLayout(self.status_grp_layout)

		self.progress_bar = QtWidgets.QProgressBar()
		self.progress_bar.setMaximum(100)
		self.progress_bar.setMinimum(0)
		self.progress_bar.setValue(0)

		self.main_layout.addWidget(self.toolbar)
		self.init_qtable_column_options()
		self.main_layout.addWidget(self.body_widget)
		self.main_layout.addWidget(self.status_grp)
		self.main_layout.addWidget(self.progress_bar)

		self.setLayout(self.main_layout)

		self.init_ui_body()
		css_file = os.path.join((os.path.dirname(__file__)), 'ui.css')
		css_content = open(css_file,"r")
		css_template = str(css_content.read())
		css_content.close()
		self.setStyleSheet(css_template)
		self.activate_qtable_columns()
	
	def init_ui_body(self):
		self.body_layout = QtWidgets.QHBoxLayout()
		self.body_layout.setContentsMargins(0,0,0,0)
		self.content_layout = QtWidgets.QVBoxLayout()

		self.content_panel = QtWidgets.QWidget()
		self.body_layout.addWidget(self.content_panel)
		self.qtable = QtWidgets.QTableWidget()
		self.qtable.setShowGrid(False)
		self.qtable.verticalHeader().setVisible(False)
		self.header = self.qtable.horizontalHeader()
		self.qtable.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
		
		self.content_layout.addWidget(self.qtable)

		self.renaming_tools = renamingToolsUI.renamingTools_UI(self)
		self.content_layout.addWidget(self.renaming_tools)

		self.content_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.body_layout.setAlignment(QtCore.Qt.AlignLeft)

		self.content_panel.setLayout(self.content_layout)
		self.body_widget.setLayout(self.body_layout)

	def init_qtable_column_options(self):
		self.qco_group = QtWidgets.QGroupBox("List Components")
		self.qco_group.setMinimumHeight(50)
		self.qco_layout = QtWidgets.QHBoxLayout()
		self.qco_group.setLayout(self.qco_layout)
		self.qco_layout.setContentsMargins(4,4,4,4)

		#This dict Contains the Listing names with their methods, all methods take the node as a parameter
		self.qtableListColumnData = {
			'Node Path':(rmCore.get_node_path),
			'Resource FilePath':(rmCore.get_file_path),
			'File Count':(self.get_formated_files_count),
			'Files Size':(self.get_formated_files_size),
			'Node Type':(self.get_formated_node_type)
		}
		self.qtableListColumnNames_in_order = ['Node Path','Resource FilePath','File Count','Files Size','Node Type']
		self.qtableColumns = []
		self.qco_checkboxes=[]
		for name in self.qtableListColumnNames_in_order:
			_label = QtWidgets.QLabel(name)
			_label.setFont(self.h2)
			_checkbox = CheckBox(data=name)
			_checkbox.setChecked(True)
			self.qco_layout.addWidget(_label)
			self.qco_layout.addWidget(_checkbox)
			self.qco_layout.addSpacing(5)
			_checkbox.clicked.connect(self.activate_qtable_columns)
			self.qco_checkboxes.append(_checkbox)
		self.qco_layout.addStretch()
		self.main_layout.addWidget(self.qco_group)
	
	def init_signals(self):
		self.qtable.itemSelectionChanged.connect(self.update_qtable)

	def activate_qtable_columns(self):

		self.qtableColumns = []

		for checkbox in self.qco_checkboxes:
			if checkbox.checkState() == QtCore.Qt.CheckState.Checked :
				self.qtableColumns.append(checkbox.data)

		if self.qtableColumns:
			self.header.show()
			self.header = self.qtable.horizontalHeader()
			self.qtable.setColumnCount(len(self.qtableColumns))
			self.qtable.setHorizontalHeaderLabels(self.qtableColumns)
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
			for i in range(len(self.qtableColumns)-1):
				self.header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
			self.header.setSectionResizeMode((len(self.qtableColumns)-1), QtWidgets.QHeaderView.Stretch)
			if self.elements :
				self.refresh_qtable()
		else:
			self.header.hide()
			self.qtable.clear()


	@staticmethod
	def get_formated_files_count(node):
		return (" " + str(rmCore.get_files_count(node)) + " files")
	
	@staticmethod
	def get_formated_files_size(node):
		file_size = str(rmCore.get_files_size(node))
		file_size_splited = file_size.split(".")
		
		rounded_decimal = ""
		for i,s in enumerate(file_size_splited[1]):
			if i > 1 :
				break
			rounded_decimal += s

		formated_size_txt = file_size_splited[0] + "." + rounded_decimal
		return (" " + formated_size_txt + "Mb")

	@staticmethod
	def get_formated_node_type(node):
		return(node.type().name())

	def refresh_qtable(self):
		count = len(self.elements)
		self.qtable.setRowCount(count)
		self.set_progressbar(0, count)
		for row in range(count):
			self.refresh_qtable_row(row)
			self.set_progressbar(row+1, count)
		self.qtable.resizeColumnsToContents()
		self.header.setSectionResizeMode((len(self.qtableColumns)-1), QtWidgets.QHeaderView.Stretch)


	def refresh_qtable_row(self, row):
		node = self.elements[row]
		for column in range(len(self.qtableColumns)):
			self.refresh_qtable_cell(node, row, column)

	
	def refresh_qtable_cell(self, node, row, column):
		'''
		Set's the value of the Qtable's given cellWidget by reading the given node
		'''
		column_name = self.qtableListColumnNames_in_order[column]
		method = self.qtableListColumnData[column_name]
		text = " " + method(node) +" "
		item = QtWidgets.QLabel(text)
		self.qtable.setCellWidget(row, column, item)

	def set_qtable_cell_value(self, new_value, row, column):
		'''
		Set's the value of the Qtable's given cellWidget using the given value
		'''
		text = " " + new_value +" "
		item = QtWidgets.QLabel(text)
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

	def set_progressbar(self, i, count):
		if count>0:
			val = (1.0*i)/count*100
		else:
			val = 0
		self.progress_bar.setValue(val)

	def update_qtable(self):
		'''
		Repopulates Qtable based on current non commited changes on elements for visualisation
		'''
		self.refresh_qtable()
		self.renaming_tools.preview_update()

	