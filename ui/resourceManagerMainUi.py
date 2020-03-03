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

class resourceManagerUI(QtWidgets.QDialog):
	def __init__(self, parent=None, pos_x=100, pos_y=100):
		super(resourceManagerUI, self).__init__(parent)
		self.version = 'alpha v0.0'
		self.setWindowTitle('Resource Manager' + ' ' + self.version)
		self.resize(1279, 677)
		self.title_font = QtGui.QFont("Calibri")
		self.title_font.setWeight(99)
		self.title_font.setPointSize(14)
		self.label_font = QtGui.QFont("Calibri")
		self.label_font.setWeight(80)
		self.label_font.setPointSize(10)
		self.move(pos_x, pos_y)
		self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
		self.elements = []

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
		self.side_panel = QtWidgets.QWidget()
		self.side_panel.setFixedWidth(250)

		self.body_layout.addWidget(self.content_panel)
		self.body_layout.addWidget(self.side_panel)

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
		self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
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
			col_elements = [(self.elements[row].path())]
			for column in range(len(self.qtableColumns)):
				file_path = rmCore.get_file_path(self.elements[row])
				col_elements.append(file_path)
				item = QtWidgets.QLabel(col_elements[column])
				self.qtable.setCellWidget(row, column, item)