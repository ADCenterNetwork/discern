import ast, sys, os
import json
from ast2json import ast2json
from io import open
from setuptools import setup

def get_name(node):
    """get_name get_name will help us ocassionally to obtain the name that the node refers to.

    Args:
        node ([ast object]): [The ast node in which we are interested to get its name.]

    Returns:
        [string]: [The name that the node refers to.]
    """
    try:
        x = node.func.id
        return x
    except AttributeError:
        try:
            x = node.func.attr 
            return x
        except AttributeError:
            try:
                x = node.id
                return x
            except AttributeError:
                try:
                    x = node.value.id
                    return x
                except AttributeError:
                    try:
                        x = node.targets[0].id
                        return x
                    except AttributeError:
                        return None

def saveast():
    """saveast is a function that will create in our directory a .txt file with a pretty print of the tree. 
    This file can help us to understand the structure of the ast.
    """
    tree = ast.parse(open(sys.argv[1]).read())
    astprint = ast2json(tree)
    f = open("astree.txt", "w",  encoding="utf8", errors='ignore')
    f.write(json.dumps(astprint, indent=4))
    f.close()

def _get_folder(filename):
    """_get_folder applies the os module to get the fullpath of a file. This is usefull because this program will open different files.

    Args:
        filename ([string]): [The name of the file we are interested.]

    Returns:
        [string]: [the full path of the file we are interested.]
    """
    path = os.path.split(filename)[0]
    return path

def self_finder(node, class_name, dc):
    if node.__class__.__name__ == 'ClassDef':
        class_name = node.name
    if node.__class__.__name__ == 'Name':
        if node.id == 'self':
            dc[node] = class_name
    for child in ast.iter_child_nodes(node):
        self_finder(child, class_name, dc)
    return dc
