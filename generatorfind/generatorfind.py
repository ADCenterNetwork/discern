import ast, sys, os
import json
from ast2json import ast2json
import time
from io import open
from setuptools import setup
import csv


#print(sys.path)
#print(os.getcwd())


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

class Discern():
    """Discern is a class that contains all the functions involved in the work with the ast of the file of interest.
	_ one inner level
	__two inner levels
	___three inner levels
    """
    def __init__(self, name):
        """we define some variables that are essential in the process of obtaining information and other variables 
        that will store the information of interest.

        Args:
            name ([string]): [The name of the file that we are obtaining information when we execute _generatorfind.py ]
        """
        self.tree = ast.parse(open(name).read())
        self.generators = []
        self.path = name
        self.calls = {}
        self.assigns = {}
        self.new_variable = None
        self.temporalassign = {}
        self.self_dictionary = self_finder(self.tree, '', {})
 
    def __yieldfind(self, node = None, ls = []):
        """Yieldfind search 'Yield's nodes and walk up the tree branch, saving all the nodes 
        that contain that generator.

        Args:
            node ([ast object], optional): [A node through which we will travel to find the yield child node. 
            At first, we will input the module object]. Defaults to None.
            ls (list, optional): [List that we record the nodes we travel until find the yield node.]. Defaults to [].
        """
        if node == None:
            node = self.tree
        if node.__class__.__name__ == 'Import':
            for i in range(len(node.names)):
                folder = _get_folder(self.path)
                importpath = node.names[i].name.split('.')
                fullpath = folder
                for j in range(len(importpath)):
                    fullpath = os.path.join(fullpath, importpath[j])
                if os.path.isfile(fullpath+'.py'):
                    if node.names[i].asname:
                        ls.append(node.names[i].asname)
                    else:
                        for item in importpath:
                            ls.append(item)
                    fileimp = fullpath+'.py'
                    treeimp = ast.parse(open(fileimp).read())
                    self.__yieldfind(treeimp, ls)
                    [ ls.pop(0) for n in range(len(importpath)+1) ]
                else: #We are in a folder. We have to modify:
                    for root, directories, files in os.walk(fullpath):
                        for filename in files:
                            fileimp2 = os.path.join(fullpath, filename)
                            if filename.endswith('.py'):
                                if node.names[i].asname:
                                    ls.append(node.names[i].asname)
                                else:
                                    filename2 = filename.split('.')
                                    ls.append(importpath[j])
                                    ls.append(filename2[0])
                                treeimp2 = ast.parse(open(fileimp2).read())
                                self.__yieldfind(treeimp2, ls)


        if node.__class__.__name__ == 'ImportFrom':
            '''In a node like this one, the attribute 'module' contains the name of the left side (from left_side
            import right_side), in the same way it's represented in code (separated by dots)

            And the attribute node.names will return a list, where each element is an 'Alias' and it represents
            the element we're importing, i.e, the right_side. To get its name we apply the attribute '.name', 

            If there is a python file, we know this either has to be on the last element of the left_side, or it 
            will be on the right side
            '''
            getfolder = _get_folder(self.path).split('/')
            if node.module == None: 
                right_side = node.names
                full_path2 = os.getcwd()
                for item in getfolder:
                    full_path2 = os.path.join(full_path2, item)
                full_path2 = full_path2.split('\\')
                if node.level > 0:
                    for i in range(node.level-1):
                        full_path2.pop(-1) 
                full_path = full_path2[0]
                full_path2.pop(0)
                variable = 0
                for item in full_path2:
                    if not variable == 0:
                        full_path = os.path.join(full_path,item)
                    else:
                        full_path = os.path.join(full_path + os.sep,item)
                        variable+=1
            else:
                left_side = node.module.split('.') 
                right_side = node.names
                #we now form a path from the elements on the left_side
                full_path2 = os.getcwd()
                for item in getfolder:
                    full_path2 = os.path.join(full_path2, item)
                full_path2 = full_path2.split('\\')
                if node.level >0:
                    for i in range(node.level-1):
                        full_path2.pop(-1)
                full_path = full_path2[0]
                full_path2.pop(0)
                variable=0
                for item in full_path2:
                    if not variable == 0:
                        full_path = os.path.join(full_path, item)
                    else:
                        full_path = os.path.join(full_path + os.sep, item)
                        variable+=1
                for item in left_side:
                    full_path = os.path.join(full_path, item)
            filename = full_path + '.py'
            if os.path.isfile(filename):
                tree2 = ast.parse(open(filename).read())
                self.__yieldfind(tree2, ls)
            #in this case, it means we have to access the right_side and look for files
            else: 
                for alias in right_side:
                    alias_filename = alias.name + '.py'
                    filename_path = os.path.join(full_path, alias_filename)
                    if os.path.isfile(filename_path):
                        #we need to append the name of the file because that's how we'll call it in the function
                        ls.append(alias) 
                        tree2 = ast.parse(open(filename_path).read())
                        self.__yieldfind(tree2, ls)        
        if node.__class__.__name__ == 'Yield':
                ls.append(node)
                x = ls[:]
                self.generators.append(x)
        else:
                if ast.iter_child_nodes(node):
                    ls.append(node)
                    for child in ast.iter_child_nodes(node):
                        y = ls[:]
                        self.__yieldfind(child, y)
        return self.generators

    def _generatorfind(self):
        """_generatorfind works with our list 'generators' in order to obtain the correct namespace instead of all the
        nodes information.
        """
        self.generators = []
        self.generators = self.__yieldfind()
        for i in range(len(self.generators)):
            k = 0
            for j in range(len(self.generators[i])-1): 
                if  self.generators[i][-j-1].__class__.__name__ == "FunctionDef" :
                    self.generators[i] = self.generators[i][1:-j]
                    break
            for m in range(len(self.generators[i])):
                j = -m - 1
                if not self.generators[i][j].__class__.__name__ =='Import' and not self.generators[i][j].__class__.__name__ =='Module':
                    if not type(self.generators[i][j]) == str:
                        self.generators[i][j] = self.generators[i][j].name
                elif self.generators[i][j].__class__.__name__ == 'Module':
                    k +=1
                elif self.generators[i][j].__class__.__name__ =='Import':
                    if self.generators[i][j].names[k-1].asname:
                        self.generators[i][j] = self.generators[i][j].names[k-1].asname
                    else:
                        self.generators[i][j] = self.generators[i][j].names[k-1].name
                elif self.generators[i][j].__class__.__name__ == 'ImportFrom':
                    if self.generators[i][j].names[k-1].asname:
                        self.generators[i][j] = self.generators[i][j].names[k-1].asname
                    elif self.generators[i][j].names[k-1].name:
                        self.generators[i][j] = self.generators[i][j].names[k-1].name
            self.generators[i] = [item for item in self.generators[i] if item.__class__.__name__ != 'Module']
        return self.generators
            
    def assign_call_find(self, node = None):
        """assign_call_find is an idea to search the call to new assignments at the moment they are assigned
         and it still is in development.

        Args:
            node ([ast object], optional): [We node we are working in. The idea is to start at the Module node
            and walk up the tree branches.]. Defaults to None.
        """
        self._generatorfind()
        if node == None:
            node = self.tree

        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.Assign):
                self.new_variable = child
                self._assignsearch(child)
            if isinstance(child, ast.Call):
                #This _findcall only detects call to our generator list.
                self._findcall(child) 
            self.assign_call_find(child)

        return self.calls
      
    def _assignsearch(self, node):
        """_assignsearch is a function that will search along the namespace of 'generators' and will call to __assignfind
        in order to find if that element has been assigned as a new variable.

        Args:
            node ([ast object], optional): [We node we are working in.]
        """
        for s in range(len(self.generators)):
            self.__assignfind(node, node,  self.generators[s][:], 0)
            if get_name(node) in self.assigns.keys() and self.assigns[get_name(node)] in self.generators:
                break


    def __assignfind(self, new_variable, node, ls, i):
        """__assignfind will travel the branches of the tree in order to detect assignments to our element of interest
        in the namespace of 'generators'.


        Args:
            node ([ast object], optional): [We node we are working in.]
            sublista([list]): [We are searching assignments of our generators in every node. In sublista we record
            the generator namespace.]
        """

        #'node' is an assign variable, and 'ls', the list we're working on 
        for child in ast.iter_child_nodes(node):
            if child.__class__.__name__ == 'Call':
                if get_name(child) in ls:
                    i = ls.index(get_name(child))
                    self.assigns[get_name(new_variable)] = [get_name(child)]
                    self.___assignfind(new_variable, child, ls, i-1)
            elif child.__class__.__name__ == 'Name':
                if get_name(child) in self.assigns.keys():
                    try:
                        if node.lineno==64:
                            print('si pasa')
                        self.assigns[node.targets[0].id] = self.assigns[get_name(child)]
                    except:
                        pass
            elif child.__class__.__name__ == 'Tuple':
                try: #We put a try/except for cases a,b = function_that_returns_two_objects. We have to include this case.
                    for j in range(len(node.value.elts)):
                        self.__assignfind_multiple(node.targets[0].elts[j], node.value.elts[j], ls)
                except AttributeError:
                    pass
            else:
                self.__assignfind(new_variable, child, ls, i)

    def __assignfind_multiple(self, left_side, right_side, ls):
        
        if right_side.__class__.__name__ == 'Call':
            if get_name(right_side) in ls:
                i = ls.index(get_name(right_side))
                self.assigns[get_name(left_side)] = [get_name(right_side)]
                self.___assignfind(left_side, right_side, ls, i-1)

        if right_side.__class__.__name__ == 'Name':
            if get_name(right_side) in self.assigns.keys():
                    self.assigns[get_name(left_side)] = self.assigns[get_name(right_side)]

    def ___assignfind(self,new_variable, node, ls, i):
        '''we want to check if any of the descendants of 'node' is in our list ls in the index i'''
        #if ast.iter_child_nodes(node) and i >= 0:
        for child in ast.iter_child_nodes(node):
            if child.__class__.__name__ == 'Call':
                if get_name(child) == ls[i]:
                    self.assigns[get_name(new_variable)].insert(0, get_name(child))
                    i = i-1
                else:
                    try:
                        del self.assigns[get_name(new_variable)]
                    except:
                        pass
            elif child.__class__.__name__ == 'Name':
                if get_name(child) in self.assigns.keys():
                    for item in self.assigns[get_name(child)]:
                        i = len(self.assigns[get_name(child)]) - 1
                        self.assigns[get_name(new_variable)].insert(0, item)
                else:
                    self.___assignfind(new_variable, child, ls, i)
            self.___assignfind(new_variable, child, ls, i)
        #else:
        #    self.assigns[get_name(new_variable)] = self.temporalassign[get_name(new_variable)]

    def _findcall(self, node):
        for sublist in self.generators:
            self.__findcall(node, sublist, len(sublist)-1) # 

    def __findcall(self, node, ls, i):
        if node.__class__.__name__ == 'Call':
            if get_name(node) == ls[i]:
                self.___findcall(node, ls, i) 
            else:
                for child in ast.iter_child_nodes(node):
                    self.__findcall(child, ls, i) 
        elif node.__class__.__name__ == 'Name':
            #we will enter here when we do not have a 'call', to check if it's an assigned variable
            if get_name(node) in self.assigns:
                i = i - len(self.assigns[get_name(node)])
                original_variables = self.assigns[get_name(node)]
                if set(original_variables).issubset(ls):
                    self.___findcall(node, ls, i)
            elif get_name(node) == ls[i]:
                self.___findcall(node, ls, i)
            elif node.id == 'self':
                if node in self.self_dictionary.keys():
                    if self.self_dictionary[node] == ls[i]:
                        self.___findcall(node, ls, i)
        elif node.__class__.__name__ == 'Attribute' and node.value.__class__.__name__ == 'Attribute':
            if node.value.attr == ls[i]:
                self.___findcall(node.value, ls, i) 
        else:
            for child in ast.iter_child_nodes(node):
                self.__findcall(child, ls, i)

    def ___findcall(self, node, ls, i):
        '''we create this function to simplify '__findcall' and add the list to our
        dictionary of calls if we're in index 0, or continue
        in __findcall otherwise'''
        if i <= 0: #if this is the case, we want to add this list as a call
            if tuple(ls) in self.calls.keys():
                if not node.lineno in self.calls[tuple(ls)]:
                    self.calls[tuple(ls)].append(node.lineno)
            else:
                self.calls[tuple(ls)] = [node.lineno]
        else: #otherwise, we want to continue the same process with its children
            for child in ast.iter_child_nodes(node):
                self.__findcall(child, ls, i-1)

class Discern2():
    """Discern2 is a class that contains all the functions involved in the work with the ast of the file of interest.
	_ one inner level
	__two inner levels
	___three inner levels
    """
    def __init__(self, name, ls_modules):
        """we define some variables that are essential in the process of obtaining information and other variables 
        that will store the information of interest.

        Args:
            name ([string]): [The name of the file that we are obtaining information when we execute _generatorfind.py ]
        """
        self.tree = ast.parse( open(name, encoding="iso-8859-15", errors='ignore').read() )
        self.generators = []
        self.path = name
        self.calls = {}
        self.assigns = {}
        self.new_variable = None
        self.modules = ls_modules
        self.temporalassign = {}
        self.self_dictionary = self_finder(self.tree, '', {})
        self.print = []
        self.sourcemap = {}
        self.sm = {}
        self.smprov = {}
        self.smdef = {}
        self.id = {}
        self.yieldsdict = {}
        self.yieldslist = []

        i = 0
        for node in ast.walk(self.tree):
            self.id[node] = i
            i+=1

    def sourcemapyield(self, node=None, ls=[]):
        if node == None:
            node = self.tree
        if node.__class__.__name__ == 'Yield':
                ls.append(node)
                x = ls[:]
                self.yieldslist.append(node)
        else:
                if ast.iter_child_nodes(node):
                    for child in ast.iter_child_nodes(node):
                        y = ls[:]
                        self.sourcemapyield(child, y)
        
        for nodoyield in self.yieldslist:
            self.yieldsdict[self.id[nodoyield]] = {"id": self.id[nodoyield], "col_offset": nodoyield.col_offset, "lineno": nodoyield.lineno}
        return self.yieldsdict
                 
    def __yieldfind(self, node = None, ls = []):
        """Yieldfind search 'Yield's nodes and walk up the tree branch, saving all the nodes 
        that contain that generator.

        Args:
            node ([ast object], optional): [A node through which we will travel to find the yield child node. 
            At first, we will input the module object]. Defaults to None.
            ls (list, optional): [List that we record the nodes we travel until find the yield node.]. Defaults to [].
        """
        if node == None:
            node = self.tree
        if node.__class__.__name__ == 'Import':
            for i in range(len(node.names)):
                folder = _get_folder(self.path)
                importpath = node.names[i].name.split('.')
                fullpath = folder
                for j in range(len(importpath)):
                    fullpath = os.path.join(fullpath, importpath[j])
                absolute_path = os.path.join(os.getcwd(), fullpath)
                if os.path.isfile(fullpath+'.py')  and (absolute_path+'.py' in self.modules):
                    if node.names[i].asname:
                        ls.append(node.names[i].asname)
                    else:
                        for item in importpath:
                            ls.append(item)
                    fileimp = fullpath+'.py'
                    treeimp = ast.parse(open(fileimp, encoding="iso-8859-15", errors='ignore').read())
                    self.__yieldfind(treeimp, ls)
                    [ ls.pop(0) for n in range(len(importpath)+1) ]
                elif absolute_path in self.modules: #We are in a folder. We have to modify:
                    if node.names[i].asname:
                        ls.append(node.names[i].asname)
                    else:
                        for item in importpath:
                            ls.append(item)
                    self.__yieldfind_folders(absolute_path, ls)


        if node.__class__.__name__ == 'ImportFrom':
            '''In a node like this one, the attribute 'module' contains the name of the left side (from left_side
            import right_side), in the same way it's represented in code (separated by dots)

            And the attribute node.names will return a list, where each element is an 'Alias' and it represents
            the element we're importing, i.e, the right_side. To get its name we apply the attribute '.name', 

            If there is a python file, we know this either has to be on the last element of the left_side, or it 
            will be on the right side
            '''
            getfolder = _get_folder(self.path).split('/')
            if node.module == None: 
                right_side = node.names
                full_path2 = os.getcwd()
                for item in getfolder:
                    full_path2 = os.path.join(full_path2, item)
                full_path2 = full_path2.split('\\')
                if node.level > 0:
                    for i in range(node.level-1):
                        full_path2.pop(-1) 
                full_path = full_path2[0]
                full_path2.pop(0)
                variable = 0
                for item in full_path2:
                    if not variable == 0:
                        full_path = os.path.join(full_path,item)
                    else:
                        full_path = os.path.join(full_path + os.sep,item)
                        variable+=1
            else:                
                left_side = node.module.split('.') 
                right_side = node.names
                #we now form a path from the elements on the left_side
                full_path2 = os.getcwd()
                for item in getfolder:
                    full_path2 = os.path.join(full_path2, item)
                full_path2 = full_path2.split('\\')
                if node.level >0:
                    for i in range(node.level-1):
                        full_path2.pop(-1)
                full_path = full_path2[0]
                full_path2.pop(0)
                variable=0
                for item in full_path2:
                    if not variable == 0:
                        full_path = os.path.join(full_path, item)
                    else:
                        full_path = os.path.join(full_path + os.sep, item)
                        variable+=1
                for item in left_side:
                    full_path = os.path.join(full_path, item)
            filename = full_path + '.py'
            
            if not filename in self.print:
                #Uncomment next lines if you want to know the status of importfroms.
                #print("* ImportFrom of", filename, "\n-> Enter:", filename in self.modules)
                #print(filename)
                self.print.append(filename)
            if os.path.isfile(filename) and (filename in self.modules):
                tree2 = ast.parse(open(filename, encoding="iso-8859-15", errors='ignore').read())
                self.__yieldfind(tree2, ls)
            #in this case, it means we have to access the right_side and look for files
            else: 
                for alias in right_side:
                    alias_filename = alias.name + '.py'
                    filename_path = os.path.join(full_path, alias_filename)
                    if os.path.isfile(filename_path) and (filename_path in self.modules):
                        #we need to append the name of the file because that's how we'll call it in the function
                        ls.append(alias) 
                        tree2 = ast.parse(open(filename_path,encoding="iso-8859-15", errors='ignore').read())
                        self.__yieldfind(tree2, ls)
        #iso-8859-15
        if node.__class__.__name__ == 'Yield':
                ls.append(node)
                x = ls[:]
                self.generators.append(x)
        else:
                if ast.iter_child_nodes(node):
                    ls.append(node)
                    for child in ast.iter_child_nodes(node):
                        y = ls[:]
                        self.__yieldfind(child, y)
        return self.generators

        
    def __yieldfind_folders(self, absolute_path, ls):
        init_filename = os.path.join(absolute_path, '__init__.py')
        if os.path.exists(init_filename):
            init_tree = ast.parse(open(init_filename, encoding="iso-8859-15", errors='ignore').read())
            self.__yieldfind(init_tree, ls)
            for node in ast.walk(init_tree):
                if node.__class__.__name__ == 'ImportFrom':
                    left_side = node.module.split('.')
                    left_side = list(filter(None, left_side))
                    right_side = node.names
                    left_side_path = absolute_path
                    for item in left_side:
                        left_side_path = os.path.join(left_side_path, item)
                    if os.path.isfile(left_side_path+'.py'):
                        filename = left_side_path+'.py'
                        tree2 = ast.parse(open(filename, encoding="iso-8859-15", errors='ignore').read())
                        self.__yieldfind(tree2, ls)


    def _generatorfind(self):
        """_generatorfind works with our list 'generators' in order to obtain the correct namespace instead of all the
        nodes information.
        """
        self.generators = []
        self.generators = self.__yieldfind()
        for i in range(len(self.generators)):
            k = 0
            for j in range(len(self.generators[i])-1): 
                if  self.generators[i][-j-1].__class__.__name__ == "FunctionDef" :
                    self.generators[i] = self.generators[i][1:-j]
                    break
            for m in range(len(self.generators[i])):
                j = -m - 1
                if not self.generators[i][j].__class__.__name__ =='Import' and not self.generators[i][j].__class__.__name__ =='Module' and not self.generators[i][j].__class__.__name__ =='If' and not self.generators[i][j].__class__.__name__ =='For' and not self.generators[i][j].__class__.__name__ =='If' and not self.generators[i][j].__class__.__name__ =='Try':
                    if not type(self.generators[i][j]) == str:
                        self.generators[i][j] = self.generators[i][j].name
                elif self.generators[i][j].__class__.__name__ == 'Module':
                    k +=1
                elif self.generators[i][j].__class__.__name__ =='Import':
                    if self.generators[i][j].names[k-1].asname:
                        self.generators[i][j] = self.generators[i][j].names[k-1].asname
                    else:
                        self.generators[i][j] = self.generators[i][j].names[k-1].name
                elif self.generators[i][j].__class__.__name__ == 'ImportFrom':
                    if self.generators[i][j].names[k-1].asname:
                        self.generators[i][j] = self.generators[i][j].names[k-1].asname
                    elif self.generators[i][j].names[k-1].name:
                        self.generators[i][j] = self.generators[i][j].names[k-1].name
                elif self.generators[i][j].__class__.__name__ =='If':
                    pass
                elif self.generators[i][j].__class__.__name__ =='For':
                    pass
                elif self.generators[i][j].__class__.__name__ =='Try':
                    pass
            self.generators[i] = [item for item in self.generators[i] if item.__class__.__name__ != 'Module']
            self.generators[i] = [item for item in self.generators[i] if item.__class__.__name__ != 'If']
            self.generators[i] = [item for item in self.generators[i] if item.__class__.__name__ != 'For']
            self.generators[i] = [item for item in self.generators[i] if item.__class__.__name__ != 'Try']
        return self.generators
            
    def assign_call_find(self, node = None):
        """assign_call_find is an idea to search the call to new assignments at the moment they are assigned
         and it still is in development.

        Args:
            node ([ast object], optional): [We node we are working in. The idea is to start at the Module node
            and walk up the tree branches.]. Defaults to None.
        """
        self._generatorfind()
        if node == None:
            node = self.tree

        for child in ast.iter_child_nodes(node):
            if self.generators == []:
                break
            if isinstance(child, ast.Assign):
                self.new_variable = child
                self._assignsearch(child)
            if isinstance(child, ast.Call):
                #This _findcall only detects call to our generator list.
                self._findcall(child) 
            self.assign_call_find(child)

        return self.calls
      
    def _assignsearch(self, node):
        """_assignsearch is a function that will search along the namespace of 'generators' and will call to __assignfind
        in order to find if that element has been assigned as a new variable.

        Args:
            node ([ast object], optional): [We node we are working in.]
        """
        for s in range(len(self.generators)):
            self.__assignfind(node, node,  self.generators[s][:], 0)
            if get_name(node) in self.assigns.keys() and self.assigns[get_name(node)] in self.generators:
                break


    def __assignfind(self, new_variable, node, ls, i):
        """__assignfind will travel the branches of the tree in order to detect assignments to our element of interest
        in the namespace of 'generators'.


        Args:
            node ([ast object], optional): [We node we are working in.]
            sublista([list]): [We are searching assignments of our generators in every node. In sublista we record
            the generator namespace.]
        """

        #'node' is an assign variable, and 'ls', the list we're working on 
        for child in ast.iter_child_nodes(node):
            if child.__class__.__name__ == 'Call':
                if get_name(child) in ls:
                    if ast.iter_child_nodes(child):
                        for childchild in ast.walk(child):
                            if get_name(childchild) in ls or get_name(childchild) in self.assigns: #and childchild != child:
                                if childchild != child:
                                    i = ls.index(get_name(child))
                                    self.assigns[get_name(new_variable)] = [get_name(child)]
                                    self.___assignfind(new_variable, child, ls, i-1)
                    else:
                        self.assigns[get_name(new_variable)] = [get_name(child)]
                        self.___assignfind(new_variable, child, ls, i-1)

            elif child.__class__.__name__ == 'Name':
                if get_name(child) in self.assigns.keys():
                    try:
                        if node.lineno==64:
                            print('si pasa')
                        self.assigns[node.targets[0].id] = self.assigns[get_name(child)]
                    except:
                        pass
            elif child.__class__.__name__ == 'Tuple':
                try: #We put a try/except for cases a,b = function_that_returns_two_objects. We have to include this case.
                    for j in range(len(node.value.elts)):
                        self.__assignfind_multiple(node.targets[0].elts[j], node.value.elts[j], ls)
                except AttributeError:
                    pass
            else:
                self.__assignfind(new_variable, child, ls, i)

    def __assignfind_multiple(self, left_side, right_side, ls):
        
        if right_side.__class__.__name__ == 'Call':
            if get_name(right_side) in ls:
                i = ls.index(get_name(right_side))
                self.assigns[get_name(left_side)] = [get_name(right_side)]
                self.___assignfind(left_side, right_side, ls, i-1)

        if right_side.__class__.__name__ == 'Name':
            if get_name(right_side) in self.assigns.keys():
                    self.assigns[get_name(left_side)] = self.assigns[get_name(right_side)]

    def ___assignfind(self,new_variable, node, ls, i):
        '''we want to check if any of the descendants of 'node' is in our list ls in the index i'''
        #if ast.iter_child_nodes(node) and i >= 0:
        for child in ast.iter_child_nodes(node):
            if child.__class__.__name__ == 'Call':
                if get_name(child) == ls[i]:
                    self.assigns[get_name(new_variable)].insert(0, get_name(child))
                    i = i-1
                else:
                    try:
                        del self.assigns[get_name(new_variable)]
                    except:
                        pass
            elif child.__class__.__name__ == 'Name':
                if get_name(child) in self.assigns.keys():
                    for item in self.assigns[get_name(child)]:
                        i = len(self.assigns[get_name(child)]) - 1
                        self.assigns[get_name(new_variable)].insert(0, item)
                else:
                    self.___assignfind(new_variable, child, ls, i)
            self.___assignfind(new_variable, child, ls, i)
        #else:
        #    self.assigns[get_name(new_variable)] = self.temporalassign[get_name(new_variable)]

    def _findcall(self, node):
        for sublist in self.generators:
            self.__findcall(node, sublist, len(sublist)-1) # 

    def __findcall(self, node, ls, i):
        if node.__class__.__name__ == 'Call':
            if get_name(node) == ls[i]:
                self.___findcall(node, ls, i) 
            else:
                for child in ast.iter_child_nodes(node):
                    self.__findcall(child, ls, i) 
        elif node.__class__.__name__ == 'Name':
            #we will enter here when we do not have a 'call', to check if it's an assigned variable
            if get_name(node) in self.assigns:
                i = i - len(self.assigns[get_name(node)])
                original_variables = self.assigns[get_name(node)]
                if set(original_variables).issubset(ls):
                    self.___findcall(node, ls, i)
            elif get_name(node) == ls[i]:
                self.___findcall(node, ls, i)
            elif node.id == 'self':
                if node in self.self_dictionary.keys():
                    if self.self_dictionary[node] == ls[i]:
                        self.___findcall(node, ls, i)
        elif node.__class__.__name__ == 'Attribute' and node.value.__class__.__name__ == 'Attribute':
            if node.value.attr == ls[i]:
                self.___findcall(node.value, ls, i) 
        else:
            for child in ast.iter_child_nodes(node):
                self.__findcall(child, ls, i)

    def ___findcall(self, node, ls, i):
        '''we create this function to simplify '__findcall' and add the list to our
        dictionary of calls if we're in index 0, or continue
        in __findcall otherwise'''
        if i <= 0: #if this is the case, we want to add this list as a call
            if tuple(ls) in self.calls.keys():
                if not node.lineno in self.calls[tuple(ls)]:
                    self.calls[tuple(ls)].append(node.lineno)
                    str1 = " "
                    if not [node, node.lineno] in self.sm[str1.join(ls)]:
                        self.sm[str1.join(ls)].append([self.id[node], node.lineno])
                        self.smprov[self.id[node]] = {"node_id": self.id[node], "line": node.lineno}
                        self.smdef[str1.join(ls)] = self.smprov

            else:
                self.calls[tuple(ls)] = [node.lineno]
                str1 = " "
                self.sm[str1.join(ls)] = [[self.id[node], node.lineno]]
                self.smprov[self.id[node]] = {"node_id": self.id[node], "line": node.lineno}
                self.smdef[str1.join(ls)] = self.smprov

                #self.sourcemap[self.path] 
        else: #otherwise, we want to continue the same process with its children
            for child in ast.iter_child_nodes(node):
                self.__findcall(child, ls, i-1)
    
    def _mapeo(self):
        
        self.sourcemap[self.path] = self.sm

        #with open('sourcemap2.json','w') as f:
        #    json.dump(str(self.sourcemap), f, indent=4)
   
        return 

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
    
    #We iterate the nodes while assigning them an id and more info, with the objective of create a source map.
    def iternodes(self, filepath, node, contador):
        self.ids[node] = [self.contador, filepath]
        padre = self.contador - 1
        if node.__class__.__name__== "Module":
            self.sourcemap[self.contador] = {"node_id": self.contador, "path":filepath, "class_name": node.__class__.__name__, "line_number": "None", "end_line_number": "None", "col_offset": "None", "end_col_offset": "None"}
        else:
            try:
                self.sourcemap[self.contador] = {"node_id": self.contador, "path":filepath, "class_name": node.__class__.__name__, "line_number": node.lineno, "end_line_number": node.end_lineno, "col_offset": node.col_offset, "end_col_offset": node.end_col_offset}
            except:
                try:
                    self.sourcemap[self.contador] = {"node_id": self.contador, "path":filepath, "class_name": node.__class__.__name__, "line_number": self.sourcemap[self.contador-1]["line_number"], "end_line_number": self.sourcemap[self.contador-1]["end_line_number"], "col_offset": node.col_offset, "end_col_offset": node.end_col_offset}
                except:
                    self.sourcemap[self.contador] = {"node_id": self.contador, "path":filepath, "class_name": node.__class__.__name__, "line_number": self.sourcemap[self.contador-1]["line_number"], "end_line_number": self.sourcemap[self.contador-1]["end_line_number"], "col_offset": "None", "end_col_offset": "None"}
        
        self.contador += 1     
        if ast.iter_child_nodes(node):
            for child in ast.iter_child_nodes(node):
                self.iternodes(filepath, child, self.contador)

    def createids(self):
        startci = time.time()
        for root, directories, files in os.walk(self.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.endswith('.py') and not filename.startswith('__init__'):
                    tree = ast.parse(open(filepath, encoding="iso-8859-15", errors='ignore').read())
                    self.iternodes(filepath, tree, self.contador)  

        #We want to create the names of the .csv and .json files.
        project = str(self.path).split('/')
        if project[-1] != '':
            nameproject = project[-1]
        else:
            nameproject = project[-2]

        #We create .json file.
        with open('sourcemap_'+nameproject+'.json','w', encoding="iso-8859-15", errors='ignore') as f:
            json.dump(self.sourcemap, f, indent=4)

        field_names = ["node_id", "path", "class_name", "line_number", "end_line_number", "col_offset", "end_col_offset"]
        write_rows = []
        for i in self.sourcemap.keys():
            write_rows.append(self.sourcemap[i])

        #We create .csv file.
        with open('sourcemap_'+nameproject+'.csv','w', encoding="iso-8859-15", errors='ignore') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names) 
            writer.writeheader() 
            writer.writerows(write_rows) 


        #Here we have, commented, a possibility to manipulate the node information because some nodes doesn't have attributes like line number.
        """
        i=0
        for root, directories, files in os.walk(self.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.endswith('.py') and not filename.startswith('__init__'):
                    for node in ast.walk(ast.parse( open(filepath, encoding="iso-8859-15", errors='ignore').read() )):
                        self.ids[node] = i

                        try:
                            self.sourcemapmanip[i] = {"path":filepath, "class_name": node.__class__.__name__, "line_number": node.lineno, "end_line_number": node.end_lineno, "col_offset": node.col_offset, "end_col_offset": node.end_col_offset}
                        except:
                            try:
                                self.sourcemapmanip[i] = {"path":filepath, "class_name": node.__class__.__name__, "line_number": self.sourcemap[i-1]["line_number"], "end_line_number": self.sourcemapmanip[str(i-1)]["end_line_number"], "col_offset": node.col_offset, "end_col_offset": node.end_col_offset}
                            except:
                                self.sourcemapmanip[i] = {"path":filepath, "class_name": node.__class__.__name__, "line_number": self.sourcemapmanip[str(i-1)]["line_number"], "end_line_number": self.sourcemapmanip[str(i-1)]["end_line_number"], "col_offset": None, "end_col_offset": None}
                        i+=1

        with open('sourcemap_manip_'+nameproject+'.json','w', encoding="iso-8859-15", errors='ignore') as f:
            json.dump(self.sourcemapmanip, f, indent=4)
        """

        endci = time.time()
        print("Tiempo sourcemap", endci-startci)

    def callsites(self):
        startdetect = time.time()

        #First step: we check the files where generators are defined, because that files are interesting in order to search calls.
        for root, directories, files in os.walk(self.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.endswith('.py') and not filename.startswith('__init__'):
                    filecode = Discern2(filepath, self.modules)
                    if filecode._generatorfind() != []:
                        self.modules.append(filepath)
        enddetect = time.time()
        print('Detectar archivos con generators en:', enddetect-startdetect)
        print(self.modules)

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
                    self.allcall[filename] = filecode.calls
        return self.allcall
