import os
import hou
import glob
from houdiniResourceManager.modules import node_manager

def is_arnold_image(node):
	return(node.type().name() == 'arnold::image')

def get_file_path(node):
    """
    Get's the file path of the given arnold image node
    :param node: the given arnold image node
    :type node: arnold::image
    :returns: the file path of the given node
    :rtype: String
    """
    return (os.path.normpath(node.parm("filename").eval()))

def set_file_path(node, new_path):
    """
    Set's the file path of the given arnold image node to the given path
    :param node: the given arnold image node
    :type node: arnold::image
    :param new_path: the new file path
    :type new_path: String
    """
    return (node.parm("filename").set(new_path))

def get_nodes(sel = False):
	nodes = []
	if sel :
		nodes = []
		for node in hou.selectedNodes():
			if is_arnold_image(node) and node :
				nodes.append(node)
			nodes += node_manager.get_nodes_by_type('arnold::image', root = node)
	else:
		nodes += node_manager.get_nodes_by_type('arnold::image')
	return nodes

def file_path_replace_by_pattern(node, pattern, replacement_pattern):
	"""
	Replaces the pattern by the given replacement in the given abc node
	"""
	pattern = os.path.normpath(pattern)
	replacement_pattern = os.path.normpath(replacement_pattern)
	abc_file_name = os.path.normpath(get_file_path(node))
	if pattern in abc_file_name :
		new_name = os.path.normpath(abc_file_name.replace(pattern,replacement_pattern))
		return (set_file_path(node,new_name))

def file_path_replace_by_pattern_in_nodes(pattern, replacement_pattern, sel=False):
	nodes = get_nodes(sel=sel)
	for node in nodes:
		file_path_replace_by_pattern(node, pattern, replacement_pattern)

def get_nodes_by_file_path_pattern(file_path_pattern, sel = False):
	nodes = get_nodes(sel = sel)
	filtered_nodes = []
	for node in nodes:
		file_path = get_file_path(node)
		if file_path_pattern in file_path:
			filtered_nodes.append(node)
	return filtered_nodes

def get_files_by_pattern(file_pattern):
	return (glob.glob(file_pattern))

def get_files(file_path):
	file_pattern = file_path.replace("<udim>","*")
	return (get_files_by_pattern(file_pattern))

def check_for_missing_file_path(node):
    file_path = get_file_path(node)
    files = get_files(file_path)
    if len(files)== 0:
        print ("Node: {} \n Has an invalid file path :\n '{}'\n".format(node.path(), file_path))

def check_for_missing_file_paths(sel = False):
	nodes = get_nodes(sel = sel)
	for node in nodes:
		check_for_missing_file_path(node)

