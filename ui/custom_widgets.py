from PySide2 import QtWidgets

class CheckBox(QtWidgets.QCheckBox):
	def __init__(self, data=None):
		super(CheckBox, self).__init__()
		self.data = data