from collections import OrderedDict
import hou
import imp
import os
import re
import subprocess
from functools import partial
from PySide2 import QtCore, QtGui, QtWidgets
from houdiniResourceManager.core import core as rmCore
from houdiniResourceManager.ui.modules import renamingToolsUI
from houdiniResourceManager.ui.modules import toolbarUI
from houdiniResourceManager.ui import custom_widgets

imp.reload(rmCore)
imp.reload(renamingToolsUI)
imp.reload(toolbarUI)
imp.reload(custom_widgets)
"""
TODO:
Inspect option in table view, which will focus on the selected node in the node view
"""


class resourceManagerUI(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super(resourceManagerUI, self).__init__(parent)
		rmCore.init_node_type_data()
		self.version = 'beta v0.0'
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
		self.node_types_to_collect = []
		self.init_ui()
		self.init_signals()
		self.init_contextual_menu()
		

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
		self.qco_layout.setSpacing(0)

		#This dict Contains the Listing names with their methods, all methods take the node as a parameter
		self.qtableListColumnData = OrderedDict()
		self.qtableListColumnData['Node Path'] = rmCore.get_node_path
		self.qtableListColumnData['Resource FilePath'] = rmCore.get_file_path
		self.qtableListColumnData['File Count'] = self.get_formated_files_count
		self.qtableListColumnData['Files Size'] = self.get_formated_files_size
		self.qtableListColumnData['Node Type'] = self.get_formated_node_type
		self.qtableColumns = []
		self.qco_checkboxes=[]
		for name in self.qtableListColumnData.keys():
			_label = QtWidgets.QLabel(name)
			_label.setFont(self.h2)
			_checkbox = custom_widgets.CheckBox(data=name)
			_checkbox.setChecked(True)
			self.qco_layout.addWidget(_checkbox)
			self.qco_layout.addWidget(_label)
			self.qco_layout.addStretch()
			_checkbox.clicked.connect(self.activate_qtable_columns)
			self.qco_checkboxes.append(_checkbox)
		
		self.main_layout.addWidget(self.qco_group)
	
	def init_signals(self):
		self.qtable.itemSelectionChanged.connect(self.update_qtable)

	def init_contextual_menu(self):
		self.qtable.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.act_open_folder = QtWidgets.QAction("Open Folder in Explorer", None)
		self.act_node_separator = QtWidgets.QAction(self.qtable)
		self.act_node_separator.setSeparator(True)
		self.act_go_to_node = QtWidgets.QAction("Select Node", None)
		self.act_copy_past_dir_separator = QtWidgets.QAction(self.qtable)
		self.act_copy_past_dir_separator.setSeparator(True)
		self.act_copy_dir_path = QtWidgets.QAction("Copy Directory Path", None)
		self.act_past_dir_path = QtWidgets.QAction("Past Directory Path", None)
		self.act_copy_past_name_separator = QtWidgets.QAction(self.qtable)
		self.act_copy_past_name_separator.setSeparator(True)
		self.act_copy_filename_path = QtWidgets.QAction("Copy FileName", None)
		self.act_past_filename_path = QtWidgets.QAction("Past FileName", None)
		self.act_sequancer_separator = QtWidgets.QAction(self.qtable)
		self.act_sequancer_separator.setSeparator(True)
		self.act_add_sequancer = QtWidgets.QAction("Add Sequancer Tag", None)

		self.act_open_folder.triggered.connect(self.ctx_open_folders_in_explorer)
		self.act_go_to_node.triggered.connect(self.ctx_go_to_node)
		self.act_copy_dir_path.triggered.connect(self.ctx_copy_file_path)
		self.act_past_dir_path.triggered.connect(self.ctx_past_file_path)
		self.act_copy_filename_path.triggered.connect(self.ctx_copy_file_name)
		self.act_past_filename_path.triggered.connect(self.ctx_past_file_name)
		self.act_add_sequancer.triggered.connect(self.ctx_add_sequancer)

		self.qtable.addAction(self.act_open_folder)
		self.qtable.addAction(self.act_node_separator)
		self.qtable.addAction(self.act_go_to_node)
		self.qtable.addAction(self.act_copy_past_dir_separator)
		self.qtable.addAction(self.act_copy_dir_path)
		self.qtable.addAction(self.act_past_dir_path)
		self.qtable.addAction(self.act_copy_past_name_separator)
		self.qtable.addAction(self.act_copy_filename_path)
		self.qtable.addAction(self.act_past_filename_path)
		self.qtable.addAction(self.act_sequancer_separator)
		self.qtable.addAction(self.act_add_sequancer)


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
	def error(message_):
		hou.ui.displayMessage(message_, title="Houdini Resource Manager")

	@staticmethod
	def query(message_):
		return (hou.ui.displayConfirmation(message_, title="Houdini Resource Manager"))

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
		column_name = self.qtableListColumnData.keys()[column]
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

	def ctx_add_sequancer(self):
		selected_rows = self.qtable_get_selected()
		selected_row_indices = [row.row() for row in selected_rows]
		selected_row_indices_count = len(selected_row_indices)
		rmCore.init_node_type_data()
		double_check = self.query("Would you like to verify and edit the sequancer placements to avoid errors?")
		for i,index in enumerate(selected_row_indices): 
			node = self.elements[index]
			file_path = rmCore.get_file_path(node)
			file_dir_name_split= os.path.split(file_path)
			file_name_ext_split = os.path.splitext(file_dir_name_split[1])
			sequancers = rmCore.node_type_data[node.type().name()]['sequance_tags']
			intevals = rmCore.node_type_data[node.type().name()]['sequance_intervals']
			if sequancers:
				if len(sequancers) > 1:
					self.error("Many sequancers are not supported yet")
				else:
					sequance_interval = intevals[0].split("-")
					regex_pattern = "("
					for i,s in enumerate(sequance_interval[0]):
						regex_pattern += "[" + s + "-" + sequance_interval[1][i] + "]"
					regex_pattern += ")"
					regex_match = re.search(regex_pattern, file_name_ext_split[0])
					new_fileName = file_name_ext_split[0][:regex_match.start() ] + sequancers[0] + file_name_ext_split[0][regex_match.end():]
					new_path = rmCore.modify_file_path(file_path, new_fileName=new_fileName)
					rmCore.modify_node(node, new_fileName=new_fileName, affect_files=False)
				self.set_progressbar(i,selected_row_indices_count)
				self.set_qtable_cell_value(new_path, index, 1)
		self.qtable.resizeColumnsToContents()


	def ctx_copy_file_name(self):
		selected_rows = self.qtable_get_selected()
		if len(selected_rows) == 1:
			app = QtGui.QGuiApplication.instance()
			clipboard = app.clipboard()
			node = self.elements[selected_rows[0].row()]
			file_path = rmCore.get_file_path(node)
			file_path_base, file_extension = os.path.splitext(file_path)
			file_path_base_split = os.path.split(file_path_base)
			string = file_path_base_split[1]
			clipboard.setText(string)
		else:
			self.error("Only One Selection Allowed for this action!")

	def ctx_copy_file_path(self):
		selected_rows = self.qtable_get_selected()
		if len(selected_rows) == 1:
			app = QtGui.QGuiApplication.instance()
			clipboard = app.clipboard()
			node = self.elements[selected_rows[0].row()]
			file_path = rmCore.get_file_path(node)
			file_path_base_split = os.path.split(file_path)
			string = file_path_base_split[0]
			clipboard.setText(string)
		else:
			self.error("Only One Selection Allowed for this action!")		
	
	def ctx_past_file_name(self):
		selected_rows = self.qtable_get_selected()
		app = QtGui.QGuiApplication.instance()
		clipboard = app.clipboard()
		string = clipboard.text()
		if self.query("Would you like to past this text as dir path '" + string + "' on selected nodes?"):
			node = self.elements[selected_rows[0].row()]
			selected_row_indices = [row.row() for row in selected_rows]
			selected_row_indices_count = len(selected_row_indices)
			for i,index in enumerate(selected_row_indices): 
				node = self.elements[index]
				rmCore.modify_node(node, new_fileName = string, affect_files=False, copy_files=False)
			self.refresh_qtable()

	def ctx_past_file_path(self):
		selected_rows = self.qtable_get_selected()
		app = QtGui.QGuiApplication.instance()
		clipboard = app.clipboard()
		string = clipboard.text()
		if self.query("Would you like to past this text as dir path '" + string + "' on selected nodes?"):
			node = self.elements[selected_rows[0].row()]
			selected_row_indices = [row.row() for row in selected_rows]
			selected_row_indices_count = len(selected_row_indices)
			for i,index in enumerate(selected_row_indices): 
				node = self.elements[index]
				rmCore.modify_node(node, new_dir = string, affect_files=False, copy_files=False)
			self.refresh_qtable()

	def ctx_go_to_node(self):
		selected_rows = self.qtable_get_selected()
		if len(selected_rows) == 1:
			node = self.elements[selected_rows[0].row()]
			node.setCurrent(True, clear_all_selected=True)
		else:
			self.error("Only One Selection Allowed for this action!")

	def ctx_open_folders_in_explorer(self):
		selected_rows = self.qtable_get_selected()
		selected_row_indices = [row.row() for row in selected_rows]
		selected_row_indices_count = len(selected_row_indices)
		for i,index in enumerate(selected_row_indices): 
			node = self.elements[index]
			file_path = rmCore.get_file_path(node)
			file_dir_name_split= os.path.split(file_path)
			subprocess.Popen(r'explorer  "' + os.path.normpath(file_dir_name_split[0]) + '"')
			self.set_progressbar(i,selected_row_indices_count)
			

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

	