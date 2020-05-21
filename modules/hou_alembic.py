from houdiniResourceManager.modules import alembic
import os
import glob

params = ['reload','fileName','frame','fps','missingfile']


def collect(from_selected=False):
    '''
    Collect Nodes from Scene
    :param from_selected: Indicates if the node collection is done from the selected node level
    :type from_selected: Boolean
    '''
    nodes = alembic.get_nodes(sel=from_selected)
    return nodes

def replace_path(nodes, from_, to_):
    from_ = os.path.normpath(from_)
    to_ = os.path.normpath(to_)
    for node in nodes:
        current_name = os.path.normpath(alembic.get_file_name(node))
        if from_ in current_name :
            new_name = current_name.replace(from_,to_)
            alembic.set_file_name(node, new_name)

def get_file_path(abc_node):
    return (os.path.normpath(abc_node.parm("fileName").eval()))

def set_file_path(abc_node, new_path):
    return (os.path.normpath(abc_node.parm("fileName").set(new_path)))

def get_files(abc_node):
    file_path = os.path.normpath(abc_node.parm("fileName").eval())
    file_path.replace("$F","*")
    return (glob.glob(file_path))