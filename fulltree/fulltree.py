import ast
import sys, os
import json
from ast2json import ast2json
from io import open

def singleton(cls):
    
    instances = dict() # diccionario de clases

    def wrap(*args, **kwargs):
        # validamos
        if cls  not in instances:
            # [clase] = instancia: "Generamos una instancia de nuestra clase"
            instances[cls] = cls(*args, **kwargs)
        
        return instances[cls]

    return wrap

@singleton
class FullTree():

    def __init__(self, rootfolder):

        self.folder = rootfolder#sys.argv[-1] # project folder  
        self.info = [0,0] # empty, no empty
        self.imports_ini = []
        self.all_ini = []
        self.body = []
        self.body_all = []
        
    def _management_imports(self, content, level, path):
        if content != []:
            imports_ini = [] # import, alias, importFrom
            aux = content.split('\n') # separo por saltos de linea
            aux_tmp = aux[:]
            for i in range(len(aux)):
                if aux[i].startswith("import"):
                    #imports_ini.insert(0, [aux[i], level, path])
                    imports_ini.insert(0, [aux[i], level])
                    aux_tmp.remove(aux[i])

                elif aux[i].startswith("from"):
                    #imports_ini.insert(0, [aux[i], level, path])
                    imports_ini.insert(0, [aux[i], level])
                    aux_tmp.remove(aux[i])  
                else:
                    pass
            return imports_ini
        
    def _management_files(self, content, imports, level):
        string = ""
        try:
            tree = ast.parse(content)
            astprint = ast2json(tree) # exception occurred
            string = json.dumps(astprint, indent=2**level)
            return string
        except:
            # pending solve exception: "Exception: unknown case for 'Ellipsis' of type '<class 'ellipsis'>'"
            # in project file: faceswap\lib\convert.py AND line exception ocurred

            pass

    def _reader(self, filename):
        # To Do: Delete comments {# and ''' """"}
        content = []
        with open(filename,'r', encoding="iso-8859-15", errors='ignore') as file:
            content = file.read()
        return str(content)

    def _save_only(self, string):
        with open('diagram.txt','w') as f:
            f.write('\n'.join(map(str, string)))

def core(pj):
    
    some_dir = pj.folder.rstrip(os.path.sep)
    num_sep = some_dir.count(os.path.sep)

    for i in os.walk(pj.folder):
        dirpath, dirname, filnames = i[0], i[1], i[2]

        for s_file in filnames:
            level = abs(num_sep-dirpath.count(os.path.sep))
            fullpath = os.path.join(dirpath, s_file)
            if s_file.endswith('.py'):
                if s_file == '__init__.py' and os.path.getsize(fullpath) == 0:
                    pj.info[0] += 1
                elif s_file == '__init__.py' and os.path.getsize(fullpath) != 0:
                    pj.info[1] += 1
                    content = pj._reader(fullpath)
                    imports_ini = pj._management_imports(content, level, dirpath.rstrip(os.path.sep))
                    pj.all_ini.insert(0, imports_ini)
                else:
                    content = pj._reader(fullpath)
                    body = pj._management_files(content, pj.imports_ini, level)
                    pj.body_all.append(body)

    pj.all_ini = list(filter(None, pj.all_ini))
    print("\nEmpty init files "+ str(pj.info[0]) +' VS '+ "NON empty init files "+ str(pj.info[1])+"\n")
    #_save_only(all_ini)
    pj._save_only(pj.body_all)

