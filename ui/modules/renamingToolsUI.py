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
        self.setFixedHeight(160)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.modification_data = {}
        self.init_ui()

        
    def init_ui(self):
        self.replaceUI = QtWidgets.QGroupBox("Replace in path")
        self.replaceUI.setMinimumWidth(350)
        self.replaceUI_layout = QtWidgets.QVBoxLayout()
        self.replaceUI_layout.setContentsMargins(0, 0, 0, 0)
        self.replaceUI.setLayout(self.replaceUI_layout)

        self.replaceUI_head_spacer = QtWidgets.QWidget()
        self.replaceUI_head_spacer.setFixedSize(0, 50)
        self.replaceUI_head_checkbox = QtWidgets.QCheckBox()
        self.replaceUI_head_label = QtWidgets.QLabel("Activate")
        if self.parent:
            self.replaceUI_head_label.setFont(self.parent.h2)
        self.replaceUI_head_Layout = QtWidgets.QHBoxLayout()
        self.replaceUI_head_Layout.setContentsMargins(0, 0, 0, 0)
        self.replaceUI_head_Layout.setAlignment(QtCore.Qt.AlignLeft)
        self.replaceUI_head_Layout.addWidget(self.replaceUI_head_spacer)
        self.replaceUI_head_Layout.addWidget(self.replaceUI_head_checkbox)
        self.replaceUI_head_Layout.addWidget(self.replaceUI_head_label)

        self.replaceUI_From_Layout = QtWidgets.QHBoxLayout()
        self.replaceUI_From_Layout.setContentsMargins(5, 0, 0, 0)
        self.replaceUI_from_label = QtWidgets.QLabel("From")
        self.replaceUI_from_edit = QtWidgets.QLineEdit()
        self.replaceUI_From_Layout.addWidget(self.replaceUI_from_label)
        self.replaceUI_From_Layout.addWidget(self.replaceUI_from_edit)
        self.replaceUI_From_Layout.addSpacing(8)

        self.replaceUI_To_Layout = QtWidgets.QHBoxLayout()
        self.replaceUI_To_Layout.setContentsMargins(20, 0, 0, 0)
        self.replaceUI_to_label = QtWidgets.QLabel("To")
        self.replaceUI_to_edit = QtWidgets.QLineEdit()
        self.replaceUI_To_Layout.addWidget(self.replaceUI_to_label)
        self.replaceUI_To_Layout.addWidget(self.replaceUI_to_edit)
        self.replaceUI_To_Layout.addSpacing(8)

        self.replaceUI_layout.addLayout(self.replaceUI_head_Layout)
        self.replaceUI_layout.addLayout(self.replaceUI_From_Layout)
        self.replaceUI_layout.addStretch()
        self.replaceUI_layout.addLayout(self.replaceUI_To_Layout)
        self.replaceUI_layout.addStretch()
        self.layout.addWidget(self.replaceUI)

        self.addUI = QtWidgets.QGroupBox("Add to File's name")
        self.addUI.setMinimumWidth(550)
        self.addUI_layout = QtWidgets.QVBoxLayout()
        self.addUI_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.addUI_layout.setContentsMargins(4, 0, 0, 0)
        self.addUI.setLayout(self.addUI_layout)


        self.addUI_prefix_Layout = QtWidgets.QHBoxLayout()
        self.addUI_prefix_Layout.setAlignment(QtCore.Qt.AlignLeft)
        self.addUI_prefix_Layout.setContentsMargins(4, 0, 0, 0)
        self.addUI_prefix_checkbox = QtWidgets.QCheckBox()
        self.addUI_prefix_label = QtWidgets.QLabel("Prefix")
        self.addUI_prefix_editbox = QtWidgets.QLineEdit()
        self.addUI_prefix_Layout.addWidget(self.addUI_prefix_checkbox)
        self.addUI_prefix_Layout.addWidget(self.addUI_prefix_label)
        self.addUI_prefix_Layout.addWidget(self.addUI_prefix_editbox)
        self.addUI_prefix_Layout.addSpacing(8)

        self.addUI_suffix_Layout = QtWidgets.QHBoxLayout()
        self.addUI_suffix_Layout.setAlignment(QtCore.Qt.AlignLeft)
        self.addUI_suffix_Layout.setContentsMargins(4, 0, 0, 0)
        self.addUI_suffix_checkbox = QtWidgets.QCheckBox()
        self.addUI_suffix_label = QtWidgets.QLabel("Suffix")
        self.addUI_suffix_editbox = QtWidgets.QLineEdit()
        self.addUI_suffix_Layout.addWidget(self.addUI_suffix_checkbox)
        self.addUI_suffix_Layout.addWidget(self.addUI_suffix_label)
        self.addUI_suffix_Layout.addWidget(self.addUI_suffix_editbox)
        self.addUI_suffix_Layout.addSpacing(8)

        self.addUI_enum_Layout = QtWidgets.QHBoxLayout()
        self.addUI_enum_Layout.setAlignment(QtCore.Qt.AlignLeft)
        self.addUI_enum_Layout.setContentsMargins(4, 0, 0, 0)       
        self.addUI_enum_checkbox = QtWidgets.QCheckBox()
        self.addUI_enum_label = QtWidgets.QLabel("Enumerate")
        self.addUI_enum_start_label = QtWidgets.QLabel("Start")
        self.addUI_enum_start_spinbox = QtWidgets.QSpinBox()
        self.addUI_enum_start_spinbox.setMaximum(9999)
        self.addUI_enum_start_spinbox.setMinimum(0)
        self.addUI_enum_by_label = QtWidgets.QLabel("By")
        self.addUI_enum_by_spinbox = QtWidgets.QSpinBox()
        self.addUI_enum_by_spinbox.setValue(1)
        self.addUI_enum_by_spinbox.setMinimum(1)
        self.addUI_enum_by_spinbox.setMaximum(9999)
        self.addUI_enum_digits_label = QtWidgets.QLabel("Digits")
        self.addUI_enum_digits_spinbox = QtWidgets.QSpinBox()
        self.addUI_enum_digits_spinbox.setValue(3)
        self.addUI_enum_digits_spinbox.setMaximum(10)
        self.addUI_enum_digits_spinbox.setMinimum(1)
        self.addUI_enum_prefix = QtWidgets.QComboBox()
        self.addUI_enum_prefix_options = ['_', '.']
        self.addUI_enum_prefix.addItems(self.addUI_enum_prefix_options)
        self.addUI_enum_placement = QtWidgets.QComboBox()
        self.addUI_enum_placement_options = ['After Suffix', 'Before Suffix']
        self.addUI_enum_placement.addItems(self.addUI_enum_placement_options)

        self.addUI_enum_Layout.addWidget(self.addUI_enum_checkbox)
        self.addUI_enum_Layout.addWidget(self.addUI_enum_label)
        self.addUI_enum_Layout.addStretch()
        self.addUI_enum_Layout.addWidget(self.addUI_enum_start_label)
        self.addUI_enum_Layout.addWidget(self.addUI_enum_start_spinbox)
        self.addUI_enum_Layout.addStretch()
        self.addUI_enum_Layout.addWidget(self.addUI_enum_by_label)
        self.addUI_enum_Layout.addWidget(self.addUI_enum_by_spinbox)
        self.addUI_enum_Layout.addStretch()
        self.addUI_enum_Layout.addWidget(self.addUI_enum_digits_label)
        self.addUI_enum_Layout.addWidget(self.addUI_enum_digits_spinbox)
        self.addUI_enum_Layout.addStretch()
        self.addUI_enum_Layout.addWidget(self.addUI_enum_prefix)
        self.addUI_enum_Layout.addStretch()
        self.addUI_enum_Layout.addWidget(self.addUI_enum_placement)
        self.addUI_enum_Layout.addSpacing(8)
        
        self.addUI_layout.addStretch()
        self.addUI_layout.addLayout(self.addUI_prefix_Layout)
        self.addUI_layout.addStretch()
        self.addUI_layout.addLayout(self.addUI_suffix_Layout)
        self.addUI_layout.addStretch()
        self.addUI_layout.addLayout(self.addUI_enum_Layout)
        self.addUI_layout.addStretch()
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
        self.ctrlsUI_oprtions_file_management_options = ['Rename Files', 'Make Copies']
        self.ctrlsUI_oprtions_file_management.addItems(self.ctrlsUI_oprtions_file_management_options)
        self.ctrlsUI_oprtions_layout.addWidget(self.ctrlsUI_oprtions_file_management)

        self.ctrlsUI_oprtions_resource_affect = QtWidgets.QComboBox()
        self.ctrlsUI_oprtions_resource_affect_options = ['Modify Files & Input', 'Modify Input']
        self.ctrlsUI_oprtions_resource_affect.addItems(self.ctrlsUI_oprtions_resource_affect_options)
        self.ctrlsUI_oprtions_layout.addWidget(self.ctrlsUI_oprtions_resource_affect)

        self.ctrlsUI_btn_apply = QtWidgets.QPushButton("Commit Changes")
        self.ctrlsUI_btn_apply.setFixedHeight(60)

        self.ctrlsUI_oprtions_layout.addWidget(self.ctrlsUI_btn_apply)

        self.ctrlsUI_layout.addWidget(self.ctrlsUI_oprtions)
        self.layout.addWidget(self.ctrlsUI)

        self.setLayout(self.layout)
        self.update_addUI_dependants()
        self.update_replace_dependants()
        self.init_signals()

    def init_signals(self):
        #Checkbox Signals
        self.replaceUI_head_checkbox.clicked.connect(self.update_replace_dependants)
        self.addUI_prefix_checkbox.clicked.connect(self.update_addUI_prefix_dependants)
        self.addUI_suffix_checkbox.clicked.connect(self.update_addUI_suffix_dependants)
        self.addUI_enum_checkbox.clicked.connect(self.update_addUI_enum_dependants)

        #Editables Signals
        self.addUI_prefix_editbox.textEdited.connect(self.collect_prefix)
        self.addUI_suffix_editbox.textEdited.connect(self.collect_suffix)
        self.replaceUI_from_edit.textEdited.connect(self.collect_replace_data)
        self.replaceUI_to_edit.textEdited.connect(self.collect_replace_data)

        self.addUI_enum_start_spinbox.valueChanged.connect(self.collect_enum)
        self.addUI_enum_by_spinbox.valueChanged.connect(self.collect_enum)
        self.addUI_enum_digits_spinbox.valueChanged.connect(self.collect_enum)
        self.addUI_enum_prefix.currentIndexChanged.connect(self.collect_enum)
        self.addUI_enum_placement.currentIndexChanged.connect(self.collect_enum)


        self.ctrlsUI_btn_apply.clicked.connect(self.preview_update)

    def collect_modification_data(self, part_separator="_"):
        self.modification_data = {}
        replace_state = self.replaceUI_head_checkbox.checkState() == QtCore.Qt.CheckState.Checked
        if replace_state : 
            self.collect_replace_from()
            if replace_from and replace_from != "":
                self.collect_replace_to()
        
        prefix_state =self.addUI_prefix_checkbox.checkState() == QtCore.Qt.CheckState.Checked
        suffix_state =self.addUI_suffix_checkbox.checkState() == QtCore.Qt.CheckState.Checked
        enum_state =self.addUI_enum_checkbox.checkState() == QtCore.Qt.CheckState.Checked
        if prefix_state:
            self.collect_prefix()
        if suffix_state:
            self.collect_suffix()
        if enum_state:
            self.collect_enum_from()
            self.collect_enum_by()
            self.collect_enum_digits()
            self.collect_enum_placement()
            self.collect_enum_prefix()


    def collect_replace_data(self):
        replace_from = self.replaceUI_from_edit.text()
        replace_to = self.replaceUI_to_edit.text()
        self.modification_data['replace_data'] = {'to': replace_to,'from': replace_from}
        self.preview_update()

    def collect_prefix(self):
        prefix = self.addUI_prefix_editbox.text()
        if prefix and prefix != "":
            self.modification_data['prefix'] = prefix
        self.preview_update()

    def collect_suffix(self):
        suffix = self.addUI_suffix_editbox.text()
        if suffix and suffix != "":
            self.modification_data['suffix'] = suffix
        self.preview_update()

    def collect_enum(self):
        self.modification_data['enum_data'] = {}
        
        enum_from = self.addUI_enum_start_spinbox.value()
        enum_by = self.addUI_enum_by_spinbox.value()
        digits = self.addUI_enum_digits_spinbox.value()
        enum_placement = self.addUI_enum_placement_options[self.addUI_enum_placement.currentIndex()]
        enum_prefixt = self.addUI_enum_prefix_options[self.addUI_enum_prefix.currentIndex()]
        self.modification_data['enum_data']['from'] = enum_from
        self.modification_data['enum_data']['by'] = enum_by
        self.modification_data['enum_data']['number of digits'] = digits
        self.modification_data['enum_data']['placement'] = enum_placement
        self.modification_data['enum_data']['prefix'] = enum_prefixt
        self.preview_update()

    def commit_changes(self):
        self.modify(commit=True)

    def get_formatted_str(self, num, num_digits):
            num_str = str(num)
            num_str_len = len(num_str)
            for i in range(num_digits - num_str_len):
                num_str = "0" + num_str
            return num_str


    def update_addUI_dependants(self):
 
        self.update_addUI_prefix_dependants()

        self.update_addUI_suffix_dependants()

        self.update_addUI_enum_dependants()

    def update_addUI_prefix_dependants(self):
        state = self.addUI_prefix_checkbox.checkState() == QtCore.Qt.CheckState.Checked
        self.addUI_prefix_editbox.setEnabled(state)
        if state:
            self.collect_prefix()
        elif 'prefix' in self.modification_data:
            del self.modification_data['prefix']
            self.preview_update()

    def update_addUI_suffix_dependants(self):
        state = self.addUI_suffix_checkbox.checkState() == QtCore.Qt.CheckState.Checked
        self.addUI_suffix_editbox.setEnabled(state)
        if state:
            self.collect_suffix()
        elif 'suffix' in self.modification_data:
            del self.modification_data['suffix']
            self.preview_update()


    def update_addUI_enum_dependants(self):
        state = self.addUI_enum_checkbox.checkState() == QtCore.Qt.CheckState.Checked
        self.addUI_enum_start_spinbox.setEnabled(state)
        self.addUI_enum_by_spinbox.setEnabled(state)
        self.addUI_enum_digits_spinbox.setEnabled(state)
        self.addUI_enum_prefix.setEnabled(state)
        self.addUI_enum_placement.setEnabled(state)
        if state:
            self.collect_enum()
        elif 'enum_data' in self.modification_data:
            del self.modification_data['enum_data']
            self.preview_update()


    def update_replace_dependants(self):
        state = self.replaceUI_head_checkbox.checkState() == QtCore.Qt.CheckState.Checked
        self.replaceUI_from_edit.setEnabled(state)
        self.replaceUI_to_edit.setEnabled(state)
        if state:
            self.collect_replace_data()
        elif 'replace_data' in self.modification_data:
            del self.modification_data['replace_data']
            self.preview_update()

    def modify(self, commit=False):
        selected_rows = self.parent.qtable_get_selected()
        selected_row_indices = [row.row() for row in selected_rows]
        for i,index in enumerate(selected_row_indices): 
            replacement_data = None
            prefix = None
            suffix = None

            if 'replace_data' in self.modification_data:
                replacement_data = self.modification_data['replace_data']
            
            if 'prefix' in self.modification_data:
                prefix = self.modification_data['prefix']

            if 'suffix' in self.modification_data:
                suffix = self.modification_data['suffix']

            if 'enum_data' in self.modification_data:

                enum_data = self.modification_data['enum_data']
                current_num  = enum_data['from'] + (enum_data['by'] * i)
                enum_str = enum_data['prefix'] + self.get_formatted_str(current_num, enum_data['number of digits'])
                if suffix:
                    if enum_data['placement'] == 'After Suffix':
                        suffix += enum_str
                    else:

                        suffix = enum_str + suffix
                else:
                    suffix = enum_str
                
            node = self.parent.elements[index]
            file_path = rmCore.get_file_path(node)
            if commit:
                node = self.parent.elements[index]
                file_path = rmCore.get_file_path(node)
                affect_files = self.ctrlsUI_oprtions_resource_affect.currentIndex() == 0
                copy_files = self.ctrlsUI_oprtions_file_management.currentIndex() == 1
                rmCore.modify_node(file_path, prefix=prefix,  replace_data=replacement_data, suffix=suffix, affect_files=affect_files, copy_files=copy_files )
            else:
                new_path = rmCore.modify_path(file_path, prefix=prefix,  replace_data=replacement_data, suffix=suffix )
                self.parent.set_qtable_cell_value(new_path, index, 1)
            self.parent.qtable.resizeColumnsToContents()

    def preview_update(self):
        self.modify(commit=False)
        
        