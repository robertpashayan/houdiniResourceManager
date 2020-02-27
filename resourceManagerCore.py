import hou
from hou_libs.resourceManager.modules import hou_alembic
from hou_libs.resourceManager.modules import hou_aImage
from hou_libs.resourceManager.modules import hou_attribfrommap
from hou_libs.resourceManager.modules import hou_file

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
