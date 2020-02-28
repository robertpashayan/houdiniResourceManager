import hou
from houdiniResourceManager.modules import hou_alembic
from houdiniResourceManager.modules import hou_aImage
from houdiniResourceManager.modules import hou_attribfrommap
from houdiniResourceManager.modules import hou_file

#common_properties to retrieve [name, path]
container_types =   ['alembic',   'arnold::image',  'attribfrommap',    'file','filecache','rop_alembic','rop_fbx','rop_geometry']
container_modules = [hou_alembic, hou_aImage,       hou_attribfrommap,  hou_file]

def collect(from_selected=False):
    nodes=[]
    for container_module in container_modules :

        container_module_nodes = container_module.collect(from_selected=from_selected)
        if container_module_nodes:
            nodes+=container_module_nodes
    return nodes

def sort_nodes(nodes):
    nodes_by_module = []
    for i in range(len(container_modules)):
        module_type = container_types[i]
        module_nodes = [node for node in nodes if node.type().name()==module_type]
        nodes_by_module.append(module_nodes)
    return nodes_by_module



def replace_path(nodes, from_, to_):
    nodes_by_modules = sort_nodes(nodes)
    acc = 0
    for mnodes in nodes_by_modules:
        container_modules[acc].replace_path(mnodes, from_, to_)
        acc+=1

def get_nodes_module(node):
    '''
    Returns the module for the given node if the node in unsupported returns None

    :param node: houdini scene node
    :returns: the module of the given node or None if node is unsupported
    '''
    node_type = node.type().name()
    if node_type in container_types:
        return (container_modules[container_types.index(node_type)])
    return None

def get_file_path(node):
    node_module = get_nodes_module(node)
    if node_module:
        return node_module.get_file_path(node)
    return None
