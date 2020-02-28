import os
from houdiniResourceManager.modules import node_manager

params = ['reload','fileName','frame','fps','missingfile']

def _get_nodes_(sel = False):
	nodes = []
	if sel :
		nodes = []
		for node in hou.selectedNodes():
			if node.type().name()=='attribfrommap':
				nodes.append(node)
			nodes += node_manager.get_nodes_by_type('attribfrommap', root = node)
	else:
		nodes += node_manager.get_nodes_by_type('attribfrommap')
	return nodes

def collect(from_selected=False):
    '''
    Collect Nodes from Scene
    :param from_selected: Indicates if the node collection is done from the selected node level
    :type from_selected: Boolean
    '''
    nodes = _get_nodes_(sel=from_selected)
    return nodes

def replace_path(nodes, from_, to_):
    from_ = os.path.normpath(from_)
    to_ = os.path.normpath(to_)
    for node in nodes:
        current_name = os.path.normpath(node.parm('filename').eval())
        if from_ in current_name :
            new_name = current_name.replace(from_,to_)
            node.parm('filename').set(new_name)