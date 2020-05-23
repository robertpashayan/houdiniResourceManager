import glob
import os
from houdiniResourceManager.modules import aImage

sequance_tags = ["<udim>"]

'''
TODO

Add an option for additional info which will indicate existing TX files
'''
params = ['reload','fileName','frame','fps','missingfile']


def collect(from_selected=False):
    '''
    Collect Nodes from Scene
    :param from_selected: Indicates if the node collection is done from the selected node level
    :type from_selected: Boolean
    '''
    nodes = aImage.get_nodes(sel=from_selected)
    return nodes

def get_file_path(node):
    return (os.path.normpath(node.parm("filename").eval()))

def get_files(node):
    file_path = os.path.normpath(node.parm("filename").eval())
    for sequance_tag in sequance_tags :
        file_path = file_path.replace(sequance_tag, "*")
    return (glob.glob(file_path))

def replace_path(nodes, from_, to_):
    from_ = os.path.normpath(from_)
    to_ = os.path.normpath(to_)
    for node in nodes:
        current_name = os.path.normpath(aImage.get_file_path(node))
        if from_ in current_name :
            new_name = current_name.replace(from_,to_)
            aImage.set_file_path(node, new_name)

def set_file_path(node, new_path):
    node.parm("filename").set(new_path)

