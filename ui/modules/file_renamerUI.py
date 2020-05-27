import hou
import imp
import os
from collections import OrderedDict
from PySide2 import QtCore, QtGui, QtWidgets
from houdiniResourceManager.core import core as rmCore

imp.reload(rmCore)

class fileRenamerItem(QtWidgets.QGroupBox):
	def __init__(self, key, data, parent, height=57):
		super(fileRenamerItem, self).__init__(key)
		self.parent = parent
		self.setFixedHeight(height)
		self.key = key
		self.data = data
		
		self.init_ui()
		self.init_signals()
		


	def init_ui(self):
		self.layout = QtWidgets.QHBoxLayout()
		self.layout.setAlignment(QtCore.Qt.AlignHCenter)
		self.setLayout(self.layout)
		if type(self.data) == list:
			self.content = QtWidgets.QComboBox()
			self.content.addItems(self.data)
			self.layout.addWidget(self.content)
		elif self.data == "*":
			self.content = QtWidgets.QLineEdit()
			self.layout.addWidget(self.content)
		elif "0-9" in self.data :
			ranges = self.data.split("-")
			self.content = QtWidgets.QSpinBox()
			self.content.setMinimumWidth(60)
			self.content.setRange(int(ranges[0]), int(ranges[1]))
			self.layout.addWidget(self.content)
		elif self.key == "Sequancer" :
			self.content = QtWidgets.QLabel(self.data)
			self.content.setMinimumWidth(70)
			self.layout.addWidget(self.content)

	def init_signals(self):
		if type(self.data) == list:
			self.content.currentIndexChanged.connect(self.parent.generate_new_fileName)
		elif self.data == "*":
			self.content.textChanged.connect(self.parent.generate_new_fileName)
		elif "0-9" in self.data :
			self.content.valueChanged.connect(self.parent.generate_new_fileName)

	def get_value(self):
		if type(self.data) == list:
			return self.data[self.content.currentIndex()]
		elif self.data == "*":
			return self.content.text()
		elif "0-9" in self.data :
			return (str(self.content.value()))
		elif self.key == "Sequancer" :
			return self.content.text()


		


class fileRenamer(QtWidgets.QDialog):
	def __init__(self, fileName, parent=None):
		super(fileRenamer, self).__init__(parent)
		if parent:
			self.setWindowTitle(self.parent.windowTitle() + " : File Renamer")
			self.setParent(parent,  QtCore.Qt.Window)
		else:
			self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
		self.fileName = fileName
		self.new_name = None
		self.setFixedHeight(150)
		self.setMinimumWidth(750)
		rmCore.init_file_name_data()
		self.node_type = rmCore.file_name_data['node_type']
		self.file_name_parts_data = rmCore.file_name_data['fileName_parts']
		self.unauthorised_characters_in_parts = rmCore.file_name_data['unauthorised_characters_in_parts']
		self.init_ui()
		self.init_signals()
		self.generate_new_fileName()


	def init_ui(self):
		self.layout = QtWidgets.QVBoxLayout()
		self.setLayout(self.layout)
		self.template_layout = QtWidgets.QHBoxLayout()
		self.control_layout = QtWidgets.QHBoxLayout()
		self.layout.addLayout(self.template_layout)
		self.layout.addLayout(self.control_layout)



		self.file_name_ui_items = OrderedDict()
		keys = self.file_name_parts_data.keys()
		for key in keys:
			if "separator" not in key:
				data = self.file_name_parts_data[key]
				item = fileRenamerItem(key, data, parent=self)
				self.template_layout.addWidget(item)
				self.file_name_ui_items[key] = item
		
		self.name_visualizer = QtWidgets.QLabel()
		self.btn_commit = QtWidgets.QPushButton("Commit")
		self.btn_commit.setFixedSize(100,40)
		self.btn_cancel = QtWidgets.QPushButton("Cancel")
		self.btn_cancel.setFixedSize(100,40)
		self.control_layout.addWidget(self.name_visualizer)
		self.control_layout.addWidget(self.btn_commit)
		self.control_layout.addWidget(self.btn_cancel)
	
	def init_signals(self):
		self.btn_commit.clicked.connect(self.commit)
		self.btn_cancel.clicked.connect(self.cancel)


	def check_name_part(self, part, key):
		error = None
		if len(part) > 0:
			try:
				part.decode('ascii')
				for ch in (self.unauthorised_characters_in_parts):
					if ch in part:
						error = "Unauthorized character '" +ch + "' in '" + key + "'!"
			except (UnicodeDecodeError, UnicodeEncodeError):
				error = "None unicode character in '" + part + "' in '" + key + "'!"
		else:
			error = "Fill the part '" + key + "' to generate a new name!"
		return error 

	def generate_new_fileName(self):
		'''
		'''
		keys = self.file_name_parts_data.keys()
		new_name = ""
		errors = []
		for key in keys:
			if "separator" not in key:
				part = self.file_name_ui_items[key].get_value()
				
				error = self.check_name_part(part, key)
				if error :
					errors.append(error)
			else:
				part = self.file_name_parts_data[key]
			
			new_name += part

		self.name_visualizer.setText(new_name)
		if not errors : 
			self.new_name = new_name
		return errors

		
	def cancel(self):
		self.new_name = None
		self.setResult(0)
		self.close()
	
	def commit(self):
		errors = self.generate_new_fileName()
		if errors :
			message_ = ""
			for error in errors:
				message_ += " - " + error + "\n"
			hou.ui.displayMessage(message_, title="Houdini Resource Manager")
		else:
			self.setResult(1)
			self.close()