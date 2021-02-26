import ast, sys, os
from ast2json import ast2json
import time
from io import open
from setuptools import setup
from .discern2 import Discern2


class FolderCalls():
    def __init__(self, name):
        self.allcall = {}
        self.path = name
        self.sourcemapfolder = {} 
        self.modules = []
        self.contador = 0


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
