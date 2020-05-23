import imp
import os
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

def get_files_count(node):
    files=get_files(node)
    return(len(files))

def get_files_size(node):
    files=get_files(node)
    size = 0
    for file_ in files:
        size += os.path.getsize(file_)
    return (size/1024.0/1024.0)

def get_node_path(node):
    return (node.path())

def get_node_specific_sequencers(node):
    node_module = get_nodes_module(node)
    if node_module:
        return node_module.sequance_tags
    return None


def modify_path(file_path, prefix=None,  replace_data=None, suffix=None ):

    file_path_base, file_extension = os.path.splitext(file_path)

    if replace_data:
        file_path_base = file_path_base.replace(replace_data["from"], replace_data["to"])

    file_path_base_split= os.path.split(file_path_base)
    new_name = file_path_base_split[1]
    if prefix:
        new_name = prefix + new_name
    
    if suffix:
        new_name = new_name + suffix
    
    return (os.path.join(file_path_base_split[0], new_name)+file_extension)

def modify_node(node, prefix=None,  replace_data=None, suffix=None, affect_files=True , copy_files=True):
    file_path = get_file_path(node)
    errors = []
    new_path = modify_path(file_path, prefix=prefix,  replace_data=replace_data, suffix=suffix )
    sane_sequancers = []
    if affect_files:
        sequance_tags =  get_node_specific_sequencers(node)
        for sequance_tag in sequance_tags:
            if sequance_tag in file_path:
                if sequance_tag in new_path :
                    sane_sequancers.append(sequance_tag)
                else:
                    errors.append("Sequancer '" + sequance_tag + "' missing after renaming, can't continue furter")
        if not errors:   
            files = get_files(node)
            sequancer_replacement_datas = []
            for sequance_tag in sane_sequancers:
                sequance_dict = {}
                sequance_dict['sequance_tag'] = sequance_tag
                sequance_dict['split_items'] = file_path.split(sequance_tag)
                sequancer_replacement_datas.append(sequance_dict)
            for file_path_ in files:
                new_file_path_ = file_path_
                for sequancer_replacement_data in sequancer_replacement_datas:
                    sequance = file_path_
                    for item in sequancer_replacement_data['split_items']:
                        sequance = sequance.replace(item, "")
                    new_file_path_ = new_path.replace(sequancer_replacement_data['sequance_tag'],sequance)
                    # print "file_path : {}\nfile_path_ : {}\nnew_file_path_: {} \nsequance:{} \nsequance_tag:{}".format(file_path, file_path_, new_file_path_, sequance, sequance_dict['sequance_tag'])
                if copy_files:
                    shutil.copyfile(file_path_, new_file_path_)
                else:
                    os.rename(file_path_, new_file_path_)        
    if not errors:
        print new_path
        set_file_path(node, new_path)
    return errors




def replace_path(nodes, from_, to_):
    nodes_by_modules = sort_nodes(nodes)
    acc = 0
    for mnodes in nodes_by_modules:
        container_modules[acc].replace_path(mnodes, from_, to_)
        acc+=1

def set_file_path(node, new_path):
    node_module = get_nodes_module(node)
    if node_module:
        node_module.set_file_path(node,new_path)
        return True
    return False

def sort_nodes(nodes):
    nodes_by_module = []
    for i in range(len(container_modules)):
        module_type = container_types[i]
        module_nodes = [node for node in nodes if node.type().name()==module_type]
        nodes_by_module.append(module_nodes)
    return nodes_by_module
