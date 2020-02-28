import hou
import os


def get_nodes(root = hou.node("/obj"), in_subnet = True, parents = False, in_sop = False):
	return (root.allSubChildren())

def get_selected():
	selected = hou.selectedNodes()
	return selected


def get_nodes_by_type(node_type, root = hou.node("/obj"), identic = True, in_subnet = True, parents = False):
	"""
	:type node_type: String
	:returns: the nodes of the given type
	:rtype: hou.ObjNode 
	"""

	nodes = get_nodes(root=root, in_subnet = in_subnet, parents = parents)
	if identic :
		filtered_nodes = [node for node in nodes if node.type().name() == node_type] 
	else:
		filtered_nodes = [node for node in nodes if node_type in node.type().name()] 
	return filtered_nodes

def get_hairs(root = hou.node("/obj"), in_subnet = True):
	return(get_nodes_by_type('hairgen', identic = False, in_subnet = in_subnet))

def get_grooms(root = hou.node("/obj"), in_subnet = True):
	return(get_nodes_by_type('guidegroom', identic = False, in_subnet = in_subnet))

def get_guideDeforms(root = hou.node("/obj"), in_subnet = True):
	return(get_nodes_by_type('guidedeform', identic = False, in_subnet = in_subnet))

def get_geometries(root = hou.node("/obj"), in_subnet = True):
	return(get_nodes_by_type('geo', in_subnet = in_subnet))

def clump_parm_value(node, parm_name, value, clump_min = False):
	for parm in  node.parms():
		if(parm.name() == parm_name):
			if clump_min:
				if(parm.eval() < value):
					parm.set(value)
			else:
				if(parm.eval() > value):
					parm.set(value)

def add_to_param_value(nodes, param_name, value):
	for node in nodes:
		for parm in  node.parms():
			if(parm.name() == param_name):
				current_value = parm.eval()
				parm.set(value+current_value)


def hide(nodes):
	for node in nodes:
		node.setDisplayFlag(False)

def show(nodes):
	for node in nodes:
		node.setDisplayFlag(True)