import ast, sys, os
import time
import csv
import json



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

class Sourcemap():
    def __init__(self, name):
        self.allcall = {}
        self.path = name
        self.sourcemapfolder = {} 
        self.modules = []
        self.ids = {}
        self.sourcemap = {}
        self.sourcemapmanip = {}
        self.contador = 0

    def main(self):
        startci = time.time()
        for root, directories, files in os.walk(self.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.endswith('.py') and not filename.startswith('__init__'):
                    tree = ast.parse(open(filepath, encoding="iso-8859-15", errors='ignore').read())
                    self.nodeIterator(filepath, tree, self.contador)  

        #We want to create the names of the .csv and .json files.
        nameproject = self.file_namesCreator()
        #We create .json file.
        self.createJson(nameproject)
        
        field_names, write_rows = self.createRows()
        #We create .csv file.
        self.createCsv(nameproject, field_names, write_rows)
        
        endci = time.time()
        print("Tiempo sourcemap", endci-startci)

    
    #We iterate the nodes while assigning them an id and more info, with the objective of create a source map.
    def nodeIterator(self, filepath, node, contador, padre = None):
        self.ids[node] = [self.contador, filepath]
        self.generateDictionaries(padre, filepath, node)
        #padre = self.contador - 1
        padre = self.contador
        self.contador += 1     
        if ast.iter_child_nodes(node):
            for child in ast.iter_child_nodes(node):
                self.nodeIterator(filepath, child, self.contador, padre)

    def generateDictionaries(self, padre, filepath, node):
        if node.__class__.__name__== "Module":
                self.sourcemap[self.contador] = {"node_id": self.contador, "path":filepath, "class_name": node.__class__.__name__, \
                "name":str(get_name(node)), "line_number": "None", "end_line_number": "None", "col_offset": "None", "end_col_offset": "None", \
                'parent_id': "None", "Generator": 0}
        else:
            try:
                self.sourcemap[self.contador] = {"node_id": self.contador, "path":filepath, "class_name": node.__class__.__name__, \
                "name":str(get_name(node)), "line_number": node.lineno, "end_line_number": node.end_lineno, "col_offset": node.col_offset, \
                "end_col_offset": node.end_col_offset, "parent_id": padre, "Generator": 0}
            except:
                self.sourcemap[self.contador] = {"node_id": self.contador, "path":filepath, "class_name": node.__class__.__name__, \
                "name":str(get_name(node)), "line_number": "None", "end_line_number": "None", "col_offset": "None", "end_col_offset": "None", \
                "parent_id": padre, "Generator": 0}

    def file_namesCreator(self):
        project = str(self.path).split('/')
        if project[-1] != '':
            nameproject = project[-1]
        else:
            nameproject = project[-2]
        return nameproject

    def createJson(self, nameproject):
        with open('sourcemap_'+nameproject+'.json','w', encoding="iso-8859-15", errors='ignore') as f:
            json.dump(self.sourcemap, f, indent=4)

    def createRows(self):
        field_names = ["node_id", "path", "class_name", "name", "line_number", \
        "end_line_number", "col_offset", "end_col_offset", "parent_id", "Generator"]
        write_rows = []
        for i in self.sourcemap.keys():
            write_rows.append(self.sourcemap[i])
        return field_names, write_rows

    def createCsv(self, nameproject, field_names, write_rows):
        with open('sourcemap_'+nameproject+'.csv','w', encoding="iso-8859-15", errors='ignore') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names) 
            writer.writeheader() 
            writer.writerows(write_rows) 