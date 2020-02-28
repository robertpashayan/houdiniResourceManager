import os
from houdiniResourceManager.modules import aImage


params = ['reload','fileName','frame','fps','missingfile']


def collect(from_selected=False):
    '''
    Collect Nodes from Scene
    :param from_selected: Indicates if the node collection is done from the selected node level
    :type from_selected: Boolean
    '''
    nodes = aImage.get_nodes(sel=from_selected)
    return nodes

def replace_path(nodes, from_, to_):
    from_ = os.path.normpath(from_)
    to_ = os.path.normpath(to_)
    for node in nodes:
        current_name = os.path.normpath(aImage.get_file_path(node))
        if from_ in current_name :
            new_name = current_name.replace(from_,to_)
            print new_name
            aImage.set_file_path(node, new_name)

def get_file_path(node):
    return (os.path.normpath(node.parm("fileName").eval()))