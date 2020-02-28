import hou
import os
from common.utils import file_parsing
from hou_libs.utils import node_manager

def is_abc(node):
	return(node.type().name() == 'alembic')

def is_node_dynamic(node):
	if is_abc(node):
		return(node.name().endswith('_DYN'))
	return False

def make_dynamic(node):
	if not (is_node_dynamic(node)):
		node.setName(node.name() + '_DYN') 

def set_file_name(abc_node, new_name):
	"""
	Sets the fileName of the given abc node to the new_one
	"""
	set_name = new_name.replace('\\', '/')
	print set_name
	if abc_node.parm("fileName").eval() != set_name:
		abc_node.parm("fileName").set(set_name)

def get_file_name(abc_node):
	"""
	Get's the fileName of the given abc node to the new_one
	"""
	return (os.path.normpath(abc_node.parm("fileName").eval()))

def replace_by_pattern(abc_node, pattern, replacement_pattern):
	"""
	Replaces the pattern by the given replacement in the given abc node
	"""
	pattern = os.path.normpath(pattern)
	replacement_pattern = os.path.normpath(replacement_pattern)
	abc_file_name = os.path.normpath(get_file_name(abc_node))
	if pattern in abc_file_name :
		new_name = os.path.normpath(abc_file_name.replace(pattern,replacement_pattern))
		return (set_file_name(abc_node,new_name))


def replace_by_pattern_in_nodes(pattern, replacement_pattern, sel=False):
	nodes = get_nodes(sel=sel)
	for node in nodes:
		replace_by_pattern(node, pattern, replacement_pattern)


def set_node_name_by_fileName(node, new_suffix = '', remove_numbered_suffix = True):
	"""
	Renames the given alemebic node by its paths file_name
	"""
	if is_abc(node):
		file_path = get_file_name(node)
		file_name =file_parsing.get_file_name(file_path)
		if remove_numbered_suffix :
			file_name = file_parsing.get_without_num_suffix(file_name)
		if new_suffix != '' :
			new_suffix = '_' + new_suffix
		node.setName(file_name + new_suffix)

def update_dynamic_node(node):
	if is_node_dynamic(node):
		file_path = get_file_name(node)
		file_name = file_parsing.get_file_name(file_path)
		num_suffix = file_parsing.get_num_suffix(file_name)
		if len(num_suffix) > 0:
			int_num = int(num_suffix)
			str_new_num = str(int_num + 1)
			for i in range(len(num_suffix)-len(str_new_num)):
				str_new_num = "0"+str_new_num
			new_file_path = file_path.replace(("_"+num_suffix+"."),("_"+str_new_num+"."))
			if (os.path.exists(new_file_path)):
				set_file_name(node, new_file_path)
				print ("file :\n'{}' loaded with success!\n".format(new_file_path))
			else:
				print ("Incrementing impossible, file :\n\'{}' does node exist!".format(new_file_path))
		else:
				print ("Numbered suffix can't be found in file:\n{}\n".format(file_path))
def get_nodes(sel = False):
	nodes = []
	if sel :
		nodes = []
		for node in hou.selectedNodes():
			if is_abc(node):
				nodes.append(node)
			nodes += node_manager.get_nodes_by_type('alembic', root = node, in_subnet=True)
	else:
		nodes += node_manager.get_nodes_by_type('alembic', in_subnet=True)
	return nodes


def set_nodes_name_by_fileName(sel = False):
	for node in get_nodes(sel = sel):
		set_node_name_by_fileName(node)
		
def make_nodes_dynamic(sel = False):
	for node in get_nodes(sel = sel):
		make_dynamic(node)

def get_dynamic_nodes(sel = False):
	for node in get_nodes(sel = sel):
		if is_node_dynamic(node):
			dyn_nodes.append(node)
	return dyn_nodes

def update_dynamic_nodes(sel = False):
	for node in get_nodes(sel = sel):
		update_dynamic_node(node)


def check_for_missing_file_path(node):
	file_path = get_file_name(node)
	if not (os.path.exists(file_path)):
		print ("Node: {} \n Has an invalid file path :\n '{}'\n".format(node.path(), file_path))

def check_for_missing_file_paths(sel = False):
	nodes = get_nodes(sel = sel)
	for node in nodes:
		check_for_missing_file_path(node)


def update_nodes_from_path(folder_path,scale=1.0, root = hou.node("/obj")):
	"""
	Scans subfolders and get's the last abc file
	If there's a GEO with that name it will update it
	Otherwise it'll create a new one
	"""
	subfolders = os.listdir(os.path.normpath(folder_path))
	abc_nodes = node_manager.get_nodes_by_type('alembic')
	for subfolder in subfolders:
		subfolder_path = os.path.join(folder_path,subfolder)
		if os.path.isdir(subfolder_path):
			abcs = os.listdir(os.path.normpath(subfolder_path))
			abcs.sort()
			last_version = abcs[len(abcs)-1]
			file_path = os.path.join(subfolder_path,last_version)
			#TODO: Check if the node exists and if so, update is otherwise do the code bellow
			status = True
			if len(abc_nodes) > 0:
				name = file_parsing.get_file_name(file_path)
				alembic_name = name[0:-4] + "_alembic_IN"
				correspondinc_abcs = [x for x in abc_nodes if x.name()==alembic_name]
				print correspondinc_abcs
				for abc in correspondinc_abcs :
					status = False
					set_file_name(abc, file_path)
			if status :
				create_import_geo_sop(file_path, scale=scale)





def create_import_geo_sop(file_path, root = hou.node("/obj"), scale = 1.0):
	name = file_parsing.get_file_name(file_path)
	name = name[0:-4]
	print name
	increment_pos = hou.Vector2(0,-1.5)
	geo_sop = root.createNode("geo")
	print (str(geo_sop))
	geo_sop.setName(name + "_GEO")

	abc_node = geo_sop.createNode("alembic")
	abc_node.setName(name+"_alembic_IN")
	abc_node_pos = abc_node.position()
	set_file_name(abc_node, file_path)

	convert_node = geo_sop.createNode("convert")
	convert_node.setInput(0,abc_node)
	convert_node.setName(name+"_convert")
	convert_node.setPosition(abc_node_pos+increment_pos)

	transform_node = geo_sop.createNode("xform")
	transform_node.setInput(0,convert_node)
	transform_node.setName(name+"_xform")
	transform_node.setPosition(abc_node_pos+increment_pos*2)
	transform_node.parm("scale").set(scale)

	out_node = geo_sop.createNode("null")
	out_node.setName("OUT")
	out_node.setInput(0,transform_node)
	out_node.setPosition(abc_node_pos+increment_pos*3)
	out_node.setDisplayFlag(True)
	out_node.setRenderFlag(True)


