import hou
import os


def get_selected():
	selected = hou.selectedNodes()
	return selected


def get_nodes_by_type(node_type, root = hou.node("/obj")):
	"""
	:type node_type: String
	:returns: the nodes of the given type
	:rtype: hou.ObjNode 
	"""

	nodes = root.allSubChildren()
	filtered_nodes = [node for node in nodes if node.type().name() == node_type] 
	return filtered_nodes

