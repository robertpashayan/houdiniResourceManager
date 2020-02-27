import os
import hou
from PySide2 import QtCore,QtGui, QtWidgets
from hou_libs.resourceManager import resourceManagerCore as rmCore

class resourceManagerUI(QtWidgets.QDialog):
	def __init__(self, parent=None, pos_x=100, pos_y=100):
		super(resourceManagerUI,self).__init__(parent)
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
		self.init_ui()
		self.elements = []

	def init_ui(self):
		# Main Sections
		self.main_layout = QtWidgets.QVBoxLayout()
		self.toolbar = QtWidgets.QWidget()
		self.body_widget = QtWidgets.QWidget()
		
		self.setLayout(self.main_layout)
		self.main_layout.addWidget(self.toolbar)
		self.main_layout.addWidget(self.body_widget)

		self.init_ui_toolbar()
		self.init_ui_body()
		self.setStyleSheet("""
							QScrollBar:vertical
							{
							border: 2px solid grey;
							background: #474747;
							width: 15px;
							margin: 22px 0 22px 0;
							}
							QScrollBar::handle:vertical {
							background: #a0a0a0;
							min-height: 20px;
							}
							QScrollBar::add-line:vertical {
							border: 2px solid grey;
							background: #474747;
							height: 20px;
							subcontrol-position: bottom;
							subcontrol-origin: margin;
							}
							QScrollBar::sub-line:vertical {
							border: 2px solid grey;
							background: #474747;
							height: 20px;
							subcontrol-position: top;
							subcontrol-origin: margin;
							}
							QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
							border: 2px solid grey;
							width: 3px;
							height: 3px;
							background: #a0a0a0;
							}

							QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
							background: none;
							}
							""")



	def init_ui_toolbar(self):
		self.toolbar.setFixedHeight(50)
		
		self.toolbar_layout = QtWidgets.QHBoxLayout()

		self.btn_scan = QtWidgets.QPushButton("Scan")
		self.btn_scan.setFixedSize(80, 40)
		self.btn_scan.clicked.connect(self.scan_scene)

		self.toolbar.setLayout(self.toolbar_layout)
		self.toolbar_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.toolbar_layout.addWidget(self.btn_scan)
		

	def init_ui_body(self):
		self.body_layout = QtWidgets.QHBoxLayout()
		self.content_layout = QtWidgets.QVBoxLayout()
		self.body_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.content_layout.setAlignment(QtCore.Qt.AlignLeft)

		self.content_panel = QtWidgets.QWidget()
		self.side_panel = QtWidgets.QWidget()
		self.side_panel.setFixedWidth(250)
		self.body_widget.setLayout(self.body_layout)
		self.body_layout.addWidget(self.content_panel)
		self.body_layout.addWidget(self.side_panel)

		self.qtable = QtWidgets.QTableWidget()
		self.qtable.verticalHeader().setVisible(False)
		self.qtableColumns = ['path','filePath']
		self.qtable.setColumnCount(len(self.qtableColumns))
		self.qtable.setHorizontalHeaderLabels(self.qtableColumns)
		self.header = self.qtable.horizontalHeader()       
		self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
		self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
		

		self.renaming_tools = QtWidgets.QWidget()
		self.renaming_tools.setFixedHeight(150)

		self.content_panel.setLayout(self.content_layout)
		self.content_layout.addWidget(self.qtable)
		self.content_layout.addWidget(self.renaming_tools)

	def refresh_qtable(self):

		self.qtable.setRowCount(len(self.elements))
		for row in range(len(self.elements)):
			col_elements = [(self.elements[row].path()),(self.elements[row].name())]
			for column in range(len(self.qtableColumns)):
				item = QtWidgets.QLabel(col_elements[column])
				self.qtable.setCellWidget(row,column, item)


		


	def scan_scene(self):
		print "scan_scene"
		self.elements = rmCore.collect()
		self.refresh_qtable()
