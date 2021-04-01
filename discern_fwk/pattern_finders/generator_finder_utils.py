import ast
import sys
import os
import json
from ast2json import ast2json
import io


class GeneratorFinderUtils:

    @classmethod
    def get_name(cls, node):
        """get_name get_name will help us ocassionally to obtain the name that the node refers to. # noqa: E501

        Args:
            node ([ast object]): [The ast node in which we are interested to get its name.] # noqa: E501

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

    @classmethod
    def saveast(cls):
        """saveast is a function that will create in our directory a .txt file with a pretty print of the tree. # noqa: E501
        This file can help us to understand the structure of the ast.
        """
        tree = ast.parse(io.open(sys.argv[1]).read())
        astprint = ast2json(tree)
        f = io.open("astree.txt", "w",  encoding="utf8", errors='ignore')
        f.write(json.dumps(astprint, indent=4))
        f.close()

    @classmethod
    def get_folder(cls, filename):
        """get_folder applies the os module to get the fullpath of a file. This is usefull because this program will open different files. # noqa: E501

        Args:
            filename ([string]): [The name of the file we are interested.]

        Returns:
            [string]: [the full path of the file we are interested.]
        """
        path = os.path.split(filename)[0]
        return path

    @classmethod
    def self_finder(cls, node, class_name, dc):
        if node.__class__.__name__ == 'ClassDef':
            class_name = node.name
        if node.__class__.__name__ == 'Name':
            if node.id == 'self':
                dc[node] = class_name
        for child in ast.iter_child_nodes(node):
            cls.self_finder(child, class_name, dc)
        return dc
