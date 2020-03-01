import os
import hou
from PySide2 import QtCore,QtGui, QtWidgets
from houdiniResourceManager import resourceManagerCore as rmCore

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
		self.elements = []
		
		self.init_ui()
		

	def init_ui(self):
		# Main Sections
		self.h2 = QtGui.QFont()
		self.h2.setPointSize(11)
		self.h2.setBold(True)


		self.main_layout = QtWidgets.QVBoxLayout()

		self.toolbar = QtWidgets.QWidget()

		self.body_widget = QtWidgets.QWidget()

		self.progress_bar = QtWidgets.QProgressBar()
		self.progress_bar.setMaximum(100)
		self.progress_bar.setMinimum(0)
		self.progress_bar.setValue(50)
		
		self.main_layout.addWidget(self.toolbar)
		self.main_layout.addWidget(self.body_widget)
		self.main_layout.addWidget(self.progress_bar)

		self.setLayout(self.main_layout)

		self.init_ui_toolbar()
		self.init_ui_body()
		css_file = os.path.join((os.path.dirname(__file__)), 'ui.css')
		css_content = open(css_file,"r")
		css_template = str(css_content.read())
		css_content.close()
		self.setStyleSheet(css_template)

		




	def init_ui_toolbar(self):
		self.toolbar.setFixedHeight(50)
		
		self.toolbar_layout = QtWidgets.QHBoxLayout()

		self.btn_scan = QtWidgets.QPushButton("Scan")
		self.btn_scan.setFixedSize(80, 48)
		self.btn_scan.clicked.connect(self.scan_scene)
		self.toolbar_layout.addWidget(self.btn_scan)
		

		self.toolbar_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.toolbar_layout.setContentsMargins(18,1,0,0)
		self.toolbar.setLayout(self.toolbar_layout)
		

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
		self.qtableColumns = ['Node Path','Resource FilePath']
		self.qtable.setColumnCount(len(self.qtableColumns))
		self.qtable.setHorizontalHeaderLabels(self.qtableColumns)
		self.qtable.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
		self.header = self.qtable.horizontalHeader()

		self.header.setStyleSheet("""
		QHeaderView::section { background-color: rgb(38, 37, 42); color: rgb(196,196,196); }
		QHeaderView::section:pressed
		{
    	background-color: rgb(43, 42, 47);
		color: white;
		}
		""")
		self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

		self.renaming_tools = QtWidgets.QWidget()
		self.renaming_tools.setFixedHeight(150)

		self.content_layout.addWidget(self.qtable)
		self.renaming_tools_ui()
		self.content_layout.addWidget(self.renaming_tools)

		self.content_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.body_layout.setAlignment(QtCore.Qt.AlignLeft)

		self.content_panel.setLayout(self.content_layout)
		self.body_widget.setLayout(self.body_layout)

	def renaming_tools_ui(self):
		self.renaming_tools_layout = QtWidgets.QHBoxLayout()

		
		self.rnm_tools_replace = QtWidgets.QWidget()
		self.rnm_tools_rplc_layout = QtWidgets.QVBoxLayout()
		self.rnm_tools_replace.setLayout(self.rnm_tools_rplc_layout)

		self.rnm_tools_rplc_head = QtWidgets.QWidget()
		self.rnm_tools_rplc_headL = QtWidgets.QCheckBox ()
		self.rnm_tools_rplc_headCh = QtWidgets.QLabel("Replace")
		self.rnm_tools_rplc_headCh.setFont(self.h2)
		self.rnm_tools_rplc_head_Layout = QtWidgets.QHBoxLayout()
		self.rnm_tools_rplc_head_Layout.setAlignment(QtCore.Qt.AlignLeft)
		self.rnm_tools_rplc_head_Layout.addWidget(self.rnm_tools_rplc_headL)
		self.rnm_tools_rplc_head_Layout.addWidget(self.rnm_tools_rplc_headCh)
		self.rnm_tools_rplc_head.setLayout(self.rnm_tools_rplc_head_Layout)

		self.rnm_tools_rplc_editFrom = QtWidgets.QWidget()
		self.rnm_tools_rplc_editFrom_Layout = QtWidgets.QHBoxLayout()
		self.rnm_tools_rplc_editFrom.setLayout(self.rnm_tools_rplc_editFrom_Layout)
		self.rnm_tools_rplc_editFromL = QtWidgets.QLabel("From")
		self.rnm_tools_rplc_editFromE = QtWidgets.QLineEdit()
		self.rnm_tools_rplc_editFrom_Layout.addWidget(self.rnm_tools_rplc_editFromL)
		self.rnm_tools_rplc_editFrom_Layout.addWidget(self.rnm_tools_rplc_editFromE)
		
		self.rnm_tools_rplc_editTo = QtWidgets.QWidget()
		self.rnm_tools_rplc_editTo_Layout = QtWidgets.QHBoxLayout()
		self.rnm_tools_rplc_editTo.setLayout(self.rnm_tools_rplc_editTo_Layout)
		self.rnm_tools_rplc_editToL = QtWidgets.QLabel("To")
		self.rnm_tools_rplc_editToE = QtWidgets.QLineEdit()
		self.rnm_tools_rplc_editTo_Layout.addWidget(self.rnm_tools_rplc_editToL)
		self.rnm_tools_rplc_editTo_Layout.addWidget(self.rnm_tools_rplc_editToE)
		

		self.rnm_tools_rplc_layout.addWidget(self.rnm_tools_rplc_head)
		self.rnm_tools_rplc_layout.addWidget(self.rnm_tools_rplc_editFrom)
		self.rnm_tools_rplc_layout.addWidget(self.rnm_tools_rplc_editTo)
		self.renaming_tools_layout.addWidget(self.rnm_tools_replace)



		self.rnm_tools_add = QtWidgets.QWidget()
		self.rnm_tools_add_layout = QtWidgets.QVBoxLayout()
		self.rnm_tools_add.setLayout(self.rnm_tools_add_layout)

		self.rnm_tools_add_head = QtWidgets.QWidget()
		self.rnm_tools_add_headL = QtWidgets.QCheckBox ()
		self.rnm_tools_add_headCh = QtWidgets.QLabel("Add")
		self.rnm_tools_add_headCh.setFont(self.h2)
		self.rnm_tools_add_head_Layout = QtWidgets.QHBoxLayout()
		self.rnm_tools_add_head_Layout.setAlignment(QtCore.Qt.AlignLeft)
		self.rnm_tools_add_head_Layout.addWidget(self.rnm_tools_add_headL)
		self.rnm_tools_add_head_Layout.addWidget(self.rnm_tools_add_headCh)
		self.rnm_tools_add_head.setLayout(self.rnm_tools_add_head_Layout)

		self.rnm_tools_add_prefix = QtWidgets.QWidget()
		self.rnm_tools_add_prefix_Layout = QtWidgets.QHBoxLayout()
		self.rnm_tools_add_prefix.setLayout(self.rnm_tools_add_prefix_Layout)
		self.rnm_tools_add_prefCh = QtWidgets.QCheckBox ()
		self.rnm_tools_add_prefL = QtWidgets.QLabel("Prefix")
		self.rnm_tools_add_prefE = QtWidgets.QLineEdit()
		self.rnm_tools_add_prefix_Layout.addWidget(self.rnm_tools_add_prefCh)
		self.rnm_tools_add_prefix_Layout.addWidget(self.rnm_tools_add_prefL)
		self.rnm_tools_add_prefix_Layout.addWidget(self.rnm_tools_add_prefE)
		
		self.rnm_tools_add_suffix = QtWidgets.QWidget()
		self.rnm_tools_add_suffix_Layout = QtWidgets.QHBoxLayout()
		self.rnm_tools_add_suffix.setLayout(self.rnm_tools_add_suffix_Layout)
		self.rnm_tools_add_prefCh = QtWidgets.QCheckBox ()
		self.rnm_tools_add_prefL = QtWidgets.QLabel("Suffix")
		self.rnm_tools_add_prefE = QtWidgets.QLineEdit()
		self.rnm_tools_add_suffix_Layout.addWidget(self.rnm_tools_add_prefCh)
		self.rnm_tools_add_suffix_Layout.addWidget(self.rnm_tools_add_prefL)
		self.rnm_tools_add_suffix_Layout.addWidget(self.rnm_tools_add_prefE)
		
		self.rnm_tools_add_enum = QtWidgets.QWidget()
		self.rnm_tools_add_enum_Layout = QtWidgets.QHBoxLayout()
		self.rnm_tools_add_enum.setLayout(self.rnm_tools_add_enum_Layout)
		self.rnm_tools_add_prefCh = QtWidgets.QCheckBox ()
		self.rnm_tools_add_prefL = QtWidgets.QLabel("Enumerate")
		self.rnm_tools_add_prefE = QtWidgets.QLineEdit()
		self.rnm_tools_add_enum_Layout.addWidget(self.rnm_tools_add_prefCh)
		self.rnm_tools_add_enum_Layout.addWidget(self.rnm_tools_add_prefL)
		self.rnm_tools_add_enum_Layout.addWidget(self.rnm_tools_add_prefE)
		
		

		self.rnm_tools_add_layout.addWidget(self.rnm_tools_add_head)
		self.rnm_tools_add_layout.addWidget(self.rnm_tools_add_prefix)
		self.rnm_tools_add_layout.addWidget(self.rnm_tools_add_suffix)
		self.rnm_tools_add_layout.addWidget(self.rnm_tools_add_enum)
		self.renaming_tools_layout.addWidget(self.rnm_tools_add)


		self.rnm_tools_options = QtWidgets.QWidget()
		self.rnm_tools_btns = QtWidgets.QWidget()

		
		self.renaming_tools_layout.addWidget(self.rnm_tools_add)
		self.renaming_tools_layout.addWidget(self.rnm_tools_options)
		self.renaming_tools_layout.addWidget(self.rnm_tools_btns)

		self.renaming_tools.setLayout(self.renaming_tools_layout)


	def refresh_qtable(self):
		self.qtable.setRowCount(len(self.elements))
		for row in range(len(self.elements)):
			
			col_elements = [(self.elements[row].path())]
			for column in range(len(self.qtableColumns)):
				file_path = rmCore.get_file_path(self.elements[row])
				col_elements.append(file_path)
				item = QtWidgets.QLabel(col_elements[column])
				self.qtable.setCellWidget(row,column, item)


		


	def scan_scene(self):
		self.elements = rmCore.collect()
		self.refresh_qtable()
