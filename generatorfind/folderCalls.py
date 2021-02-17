import ast, sys, os
import json
from ast2json import ast2json
import time
from io import open
from setuptools import setup
import csv
from .discern2 import Discern2

class FolderCalls():
    def __init__(self, name):
        self.allcall = {}
        self.path = name
        self.sourcemapfolder = {} 
        self.modules = []
        self.ids = {}
        self.sourcemap = {}
        self.sourcemapmanip = {}
        self.contador = 0
        self.node_classification = {}

    def labelCreator(self):
        startci = time.time()
        folder_path = self.createFolderForLabels()
        for root, directories, files in os.walk(self.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.endswith('.py') and not filename.startswith('__init__'):
                    tree = ast.parse(open(filepath, encoding="iso-8859-15", errors='ignore').read())
                    self.nodeAttributeCreator(filepath, tree, self.contador)  
                    #We create .csv file.
                    self.labelFileCreator(filename, folder_path)

        endci = time.time()
        print("Tiempo nodeToNumber", endci-startci)
    
    def createFolderForLabels(self):
        nameproject = self.getNameProject()
        path = "LabelFolder_" + nameproject
        path = os.path.join(os.getcwd(), path)
        try:
            os.mkdir(path)
        except FileExistsError:
            os.rmdir(path)
            os.mkdir(path)
        return path
    
    #We iterate the nodes while assigning them an id and more info, with the objective of create a source map.
    def nodeAttributeCreator(self, filepath, node, contador, padre = None):
        self.ids[node] = [self.contador, filepath]
        self.nodeToNumber()
        #padre = self.contador - 1
        if node.__class__.__name__== "Module":
            self.sourcemap[self.contador] = { "class_name": self.node_classification[node.__class__.__name__], "parent_id": -1, "Generator": 0}
        else:
            try:
                self.sourcemap[self.contador] = {"class_name": self.node_classification[node.__class__.__name__], "parent_id": padre, "Generator": 0}
            except:
                self.sourcemap[self.contador] = {"class_name": self.node_classification[node.__class__.__name__], "parent_id": padre, "Generator": 0}
        padre = self.contador
        self.contador += 1     
        if ast.iter_child_nodes(node):
            for child in ast.iter_child_nodes(node):
                self.nodeAttributeCreator(filepath, child, self.contador, padre)

    def nodeToNumber(self):
        file_path = os.path.join(sys.path[0], 'typenodes.txt')
        with open(file_path) as f:
            i = 0
            for node_type in f:
                node_type = node_type.split('\n')[0]
                self.node_classification[node_type] = i
                i += 1

    
    
    def getNameProject(self):
        return os.path.basename(os.path.normpath(self.path))


    
    def labelFileCreator(self, nameproject, folder_path):
        field_names = ["class_name", "parent_id", "Generator"]
        write_rows = self.writeRows()
        file_path = os.path.join(folder_path, 'label_'+nameproject+'.csv')
        with open(file_path,'w', encoding="iso-8859-15", errors='ignore') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names) 
            writer.writeheader() 
            writer.writerows(write_rows) 

    def writeRows(self):
        write_rows = []
        for i in self.sourcemap.keys():
            write_rows.append(self.sourcemap[i])
        return write_rows

    def files_with_generators(self):
        startdetect = time.time()
        #First step: we check the files where generators are defined, because that files are interesting in order to search calls.
        for root, directories, files in os.walk(self.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.endswith('.py') and not filename.startswith('__init__'):
                    filecode = Discern2(filepath, [])
                    if filecode._generatorfind() != []:
                        self.modules.append(filepath)
        enddetect = time.time()
        print('Detectar archivos con generators en:', enddetect-startdetect)
        print(self.modules)

    def callsites(self):
        #Next step: for every .py file at the project, we search callsites of that generators.
        for root, directories, files in os.walk(self.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.endswith('.py') and not filename.startswith('__init__'):
                    filecode = Discern2(filepath, self.modules)
                    filecode._generatorfind
                    startacf = time.time()
                    filecode.assign_call_find()
                    endacf = time.time()
                    print('Tiempo en assigncallfind para', filename, endacf-startacf)
                    #self.allcall[filename] = filecode.assign_call_find()
                    #I think next line should be removed.
                    self.sourcemapfolder[str(filepath)] = {"yields":filecode.sourcemapyield(), "callsites": filecode.smdef}
                    if filecode.calls != {}:
                        self.allcall[filename] = filecode.calls
        return self.allcall
