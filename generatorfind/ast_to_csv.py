import ast, sys, os, shutil
import time
import csv


def onerror(func, path, exc_info):
        """
        Error handler for ``shutil.rmtree``.

        From https://stackoverflow.com/a/2656405

        If the error is due to an access error (read only file)
        it attempts to add write permission and then retries.

        If the error is for another reason it re-raises the error.

        Usage : ``shutil.rmtree(path, onerror=onerror)``
        """
        import stat
        if not os.access(path, os.W_OK):
            # Is the error an access error ?
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise Exception("Cannot delete dir with shutil.rmtree")


def nukedir(dir):
    if dir[-1] == os.sep: dir = dir[:-1]
    files = os.listdir(dir)
    for file in files:
        if file == '.' or file == '..': continue
        path = dir + os.sep + file
        if os.path.isdir(path):
            nukedir(path)
        else:
            os.unlink(path)
    os.rmdir(dir)

def createDirectory(path):
    try:
            os.mkdir(path)
    except FileExistsError:
        try:
            shutil.rmtree(path)
            os.mkdir(path)
        except Exception:
            i = 0
            while True:
                try:
                    path = os.path.join(path, str(i))
                    os.mkdir(path)
                    break
                except FileExistsError:
                    i += 1


class AstToCsv():
    def __init__(self, name):
        self.path = name
        self.dict_with_gen = {}
        self.dict_no_gen = {}
        self.contador = 0
        self.node_classification = {}

    def main(self):
        startci = time.time()
        folders_path_tuple = self.createFolderForLabels()
        for root, directories, files in os.walk(self.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.endswith('.py') and not filename.startswith('__init__'):
                    tree = ast.parse(open(filepath, encoding="iso-8859-15", errors='ignore').read())
                    self.nodeAttributeCreator(filepath, tree, self.contador)  
                    #We create .csv file.
                    self.labelFileCreator(filename, folders_path_tuple)

        endci = time.time()
        print("Tiempo nodeToNumber", endci-startci)
    
    def createFolderForLabels(self):
        nameproject = self.getNameProject()
        path = "LabelFolder_" + nameproject
        path = os.path.join(os.getcwd(), path)
        createDirectory(path)
        path_subfolder1 = os.path.join(path, 'LabelFolderWithGen_' + nameproject)
        path_subfolder2 = os.path.join(path, 'LabelFolderNoGen_' + nameproject)
        createDirectory(path_subfolder1)
        createDirectory(path_subfolder2)
        return (path_subfolder1, path_subfolder2)

        
    #We iterate the nodes while assigning them an id and more info, with the objective of create a source map.
    def nodeAttributeCreator(self, filepath, node, contador, padre = None):
        #self.ids[node] = [self.contador, filepath]
        self.nodeToNumber()
        #padre = self.contador - 1
        self.dictionaryCreator(node, padre)
        padre = self.contador
        self.contador += 1     
        if ast.iter_child_nodes(node):
            for child in ast.iter_child_nodes(node):
                self.nodeAttributeCreator(filepath, child, self.contador, padre)

    def dictionaryCreator(self, node, padre):
        if node.__class__.__name__== "Module":
            self.dict_with_gen[self.contador] = {"node_id":self.contador, "class_name": self.node_classification[node.__class__.__name__], "parent_id": -1, "Generator": 0}
            self.dict_no_gen[self.contador] = {"node_id":self.contador, "class_name": self.node_classification[node.__class__.__name__], "parent_id": -1}
        else:
            try:
                self.dict_with_gen[self.contador] = {"node_id":self.contador,"class_name": self.node_classification[node.__class__.__name__], "parent_id": padre, "Generator": 0}
                self.dict_no_gen[self.contador] = {"node_id":self.contador,"class_name": self.node_classification[node.__class__.__name__], "parent_id": padre}
            except:
                self.dict_with_gen[self.contador] = {"node_id":self.contador,"class_name": self.node_classification[node.__class__.__name__], "parent_id": padre, "Generator": 0}
                self.dict_no_gen[self.contador] = {"node_id":self.contador,"class_name": self.node_classification[node.__class__.__name__], "parent_id": padre}

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


    
    def labelFileCreator(self, nameproject, folders_path_tuple):
        field_names = [["node_id", "class_name", "parent_id", "Generator"], ["node_id", "class_name", "parent_id"]]
        write_rows = self.writeRows()
        i = 0
        for folder_path in folders_path_tuple:
            file_path = os.path.join(folder_path, 'label_'+nameproject+'.csv')
            with open(file_path,'w', encoding="iso-8859-15", errors='ignore') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = field_names[i]) 
                writer.writeheader() 
                writer.writerows(write_rows[i]) 
                i += 1

    def writeRows(self):
        write_rows_with_gen = []
        write_rows_no_gen = []
        for i in self.dict_with_gen.keys():
            write_rows_with_gen.append(self.dict_with_gen[i])
        for i in self.dict_no_gen.keys():
            write_rows_no_gen.append(self.dict_no_gen[i])
        return write_rows_with_gen, write_rows_no_gen

