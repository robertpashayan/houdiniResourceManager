import hou
import imp
import shutil


from houdiniResourceManager.modules import hou_alembic
from houdiniResourceManager.modules import hou_aImage
from houdiniResourceManager.modules import hou_attribfrommap
from houdiniResourceManager.modules import hou_file



imp.reload(hou_alembic)
imp.reload(hou_aImage)
imp.reload(hou_attribfrommap)
imp.reload(hou_file)

#common_properties to retrieve [name, path]
container_types =   ['alembic',   'arnold::image',  'attribfrommap',    'file','filecache','rop_alembic','rop_fbx','rop_geometry']
# container_types =   ['arnold::image']
container_modules = [hou_alembic, hou_aImage,       hou_attribfrommap,  hou_file]
container_modules_activation_state = [False for x in container_modules]
# container_modules = [hou_aImage]

def collect(from_selected=False):
    nodes=[]
    for i,container_module in enumerate(container_modules):
        if container_modules_activation_state[i]:
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

def get_files(node):
    node_module = get_nodes_module(node)
    if node_module:
        return node_module.get_files(node)
    return None

def set_file_path(node, new_path, modify_files=False, copy = False):
    node_module = get_nodes_module(node)
    if node_module:
        current_file_path = node_module.get_file_path(node)
        if current_file_path != new_path :
            if modify_files :
                files = node_module.get_files(node)
                new_files = []
                for file_ in files:
                    new_file = file_
                    for sequance_tag in node_module.sequance_tags :
                        sequance_tag_length = len(sequance_tag)
                        if sequance_tag in current_file_path :                
                            sequance_tag_index_from = current_file_path.index(sequance_tag)
                            sequand_tag_index_to = file_.index(current_file_path[sequance_tag_index_from+sequance_tag_length:])
                            sequance_part = file_[sequance_tag_index_from:sequand_tag_index_to]
                            assert sequance_tag in new_path, "New path %r doesn't have the same sequance tag %r!" % (new_path,  sequance_part)
                            new_file = new_path.replace(sequance_tag, sequance_part)
                    new_files.append(new_file)
                
                for i,new_file in enumerate(new_files) :
                    old_file = files[i]
                    if copy :
                        # shutil.copyfile(old_file, new_file)
                        print ("Copying the file :\n{}\nTo :\n{}\n".format(old_file,new_file))
                    else:
                        # shutil.move(old_file, new_file)
                        print ("Renaming the file :\n{}\nTo :\n{}\n".format(old_file,new_file))            
            # node_module.set_file_path(node,new_path)
        return True
    return False