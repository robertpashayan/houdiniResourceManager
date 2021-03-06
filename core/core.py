from collections import OrderedDict
import glob
import imp
import json
import os
import shutil


from houdiniResourceManager.core import node_manager
imp.reload(node_manager)

node_type_data = None
file_name_data = None
class JSON_Loading_Error(Exception):
		pass

def init_file_name_data():
	'''
	Set's the global variable config the configuration fetched from the json file "node_type_data.json" in config directory
	'''
	global file_name_data
	

	this_dir = os.path.dirname((os.path.dirname(__file__)))
	json_file_path = os.path.normpath(os.path.join(this_dir,"config","fileName_template.json"))
	
	if json_file_path and os.path.exists(json_file_path):
		with open(json_file_path, 'r') as file:
			file_name_data = json.load(file, object_pairs_hook=OrderedDict)

	else:
		raise JSON_Loading_Error("JSON file '" + os.path.normpath(json_file_path) + "' does not exist!")

def init_node_type_data():
	'''
	Set's the global variable config the configuration fetched from the json file "node_type_data.json" in config directory
	'''
	global node_type_data
	

	this_dir = os.path.dirname((os.path.dirname(__file__)))
	json_file_path = os.path.normpath(os.path.join(this_dir,"config","node_type_data.json"))
	
	if json_file_path and os.path.exists(json_file_path):
		with open(json_file_path, 'r') as file:
			node_type_data = json.load(file, object_pairs_hook=OrderedDict)

	else:
		raise JSON_Loading_Error("JSON file '" + os.path.normpath(json_file_path) + "' does not exist!")


def collect(module_names, from_selected=False):
	nodes=[]
	for module_name in module_names:
		module_nodes = node_manager.get_nodes_by_type(module_name)
		if module_nodes:
			nodes+=module_nodes
	return nodes

def get_file_path(node):
	global node_type_data
	if node_type_data:
		file_name_parm = node_type_data[node.type().name()]['file_name_param']
		return (os.path.normpath(node.parm(file_name_parm).eval()))
	return None

def get_files(node):
	global node_type_data
	if node_type_data:
		file_path = get_file_path(node)
		sequance_tags = node_type_data[node.type().name()]['sequance_tags']
		for sequance_tag in sequance_tags :
			file_path = file_path.replace(sequance_tag, "*")
		return (glob.glob(file_path))
	return None

def get_files_count(node):
	files = get_files(node)
	return(len(files))

def get_files_size(node):
	files = get_files(node)
	size = 0
	for file_ in files:
		size += os.path.getsize(file_)
	return (size/1024.0/1024.0)

def get_node_path(node):
	return (node.path())

def get_node_specific_sequencers(node):
	global node_type_data
	if node_type_data:
		return (node_type_data[node.type().name()]['sequance_tags'])
	return None


def modify_file_path(file_path, cut_data = None, new_dir = None, new_fileName = None, prefix=None,  replace_data=None, suffix=None ):

	file_path_base, file_extension = os.path.splitext(file_path)


	file_path_base_split = os.path.split(file_path_base)
	directory_ = file_path_base_split[0]
	new_name = file_path_base_split[1]
	if new_fileName:
		new_name = new_fileName
	else:
		if cut_data:
			new_name = new_name[:cut_data["from"]] +  new_name[cut_data["to"]:]
		if replace_data:
			new_name = new_name.replace(replace_data["from"], replace_data["to"])
		if prefix:
			new_name = prefix + new_name

		if suffix:
			new_name = new_name + suffix

	if new_dir:
		directory_ = new_dir

	return (os.path.join(directory_, new_name)+file_extension)

def modify_node(node, cut_data = None, new_dir=None,  new_fileName = None, prefix=None,  replace_data=None, suffix=None, affect_files=True , copy_files=True):
	file_path = get_file_path(node)
	errors = []
	new_path = modify_file_path(file_path, cut_data = cut_data, new_dir=new_dir, new_fileName=new_fileName, prefix=prefix,  replace_data=replace_data, suffix=suffix )
	sane_sequancers = []
	if affect_files:
		sequance_tags =  get_node_specific_sequencers(node)
		for sequance_tag in sequance_tags:
			if sequance_tag in file_path:
				if sequance_tag in new_path :
					sane_sequancers.append(sequance_tag)
				else:
					errors.append("Sequancer '" + sequance_tag + "' missing after renaming, can't continue furter")
		if not errors:   
			files = get_files(node)
			sequancer_replacement_datas = []
			for sequance_tag in sane_sequancers:
				sequance_dict = {}
				sequance_dict['sequance_tag'] = sequance_tag
				sequance_dict['split_items'] = file_path.split(sequance_tag)
				sequancer_replacement_datas.append(sequance_dict)
			for file_path_ in files:
				new_file_path_ = file_path_
				for sequancer_replacement_data in sequancer_replacement_datas:
					sequance = file_path_
					for item in sequancer_replacement_data['split_items']:
						sequance = sequance.replace(item, "")
					new_file_path_ = new_path.replace(sequancer_replacement_data['sequance_tag'],sequance)
				if copy_files:
					shutil.copyfile(file_path_, new_file_path_)
				else:
					os.rename(file_path_, new_file_path_)        
	if not errors:
		set_file_path(node, new_path)
	return errors

def set_file_path(node, new_path):
	global node_type_data
	if node_type_data:
		file_name_parm = node_type_data[node.type().name()]['file_name_param']
		node.parm(file_name_parm).set(new_path)
		return True
	return False