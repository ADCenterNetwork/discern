import ast
import sys, os
import json
from ast2json import ast2json
import time

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
    f = open("astree.txt", "w")
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

def _management_imports(content, level, path):
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
    
def _management_files(content, imports, level):
    tree = ast.parse(content)
    astprint = ast2json(tree)
    string = json.dumps(astprint, indent=2**level)
    return string

def _reader(filename):
    content = []
    with open(filename, encoding='iso-8859-15') as file:
        #try:
            for line in file:
                if line.startswith('#'):# or line.startswith(' """ ') or line.endswith(' """ '):
                    continue  # skip comments
                content.append(line.strip())
        #except: UnicodeDecodeError
    return str(content)

def _save_only(string):
    with open('diagram.txt','w') as f:
        f.write('\n'.join(map(str, string)))

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
            left_side = node.module.split('.') 
            right_side = node.names
            #we now form a path from the elements on the left_side
            full_path = os.path.join(os.getcwd(), _get_folder(self.path))
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
        self.tree = ast.parse(open(name).read())
        self.generators = []
        self.path = name
        self.calls = {}
        self.assigns = {}
        self.new_variable = None
        self.modules = ls_modules
        self.temporalassign = {}
        self.self_dictionary = self_finder(self.tree, '', {})
        self.print = []
 
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
                    treeimp = ast.parse(open(fileimp).read())
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
            left_side = node.module.split('.') 
            right_side = node.names
            #we now form a path from the elements on the left_side
            full_path = os.path.join(os.getcwd(), _get_folder(self.path))
            for item in left_side:
                full_path = os.path.join(full_path, item)
            filename = full_path + '.py'
            
            if not filename in self.print:
                print("Tenemos un ImportFrom al archivo", filename, "\n y queremos entrar en alguno de los siguientes paths:\n", self.modules, "\n Coincide con alguno:", filename in self.modules)
                self.print.append(filename)
            if os.path.isfile(filename) and (filename in self.modules):
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

        
    def __yieldfind_folders(self, absolute_path, ls):
        init_filename = os.path.join(absolute_path, '__init__.py')
        if os.path.exists(init_filename):
            init_tree = ast.parse(open(init_filename).read())
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
                        tree2 = ast.parse(open(filename).read())
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


class FolderCalls():
    def __init__(self, name):
        self.allcall = {}
        self.path = name
        
    def callsites(self):
        for root, directories, files in os.walk(self.path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if filename.endswith('.py'):
                    filecode = Discern(filepath)
                    self.allcall[filename] = filecode.assign_call_find()
        return self.allcall

def main(name):
    start = time.time()
    if len(sys.argv) == 2:
        if name.endswith('.py'):
            print("***************************************\n")
            print("***Estamos trabajando con DISCERN1.***\n")
            print("***************************************\n")
            script = Discern(name)
            saveast()      
            #script.yieldfind()
            '''
            print('-----------------------------------------------------------------------------------------------------\n')
            print('In the following list we find the node\'s namespace of the generators defined in the script of interest:')
            for i in range(len(script.generators)):
                print('\n', i, ': \n', script.generators[i])
            print("----------")
            '''
            #script._generatorfind()
            '''
            print('In the following list we find the namespace of the generators defined in the script of interest:')
            for i in range(len(script.generators)):
                print('\n', i, ': \n', script.generators[i])
            print("----------")
            '''
            print(script._generatorfind())
            script.assign_call_find()
        else:
            print("***************************************\n")
            print("***Estamos trabajando con FOLDER.***\n")
            print("***************************************\n")
            script = FolderCalls(name)
            script.callsites()
        
        print('LOS ASSIGNS SON LOS SIGUIENTES: ', script.assigns)
        print('LOS CALLS QUE HEMOS ENCONTRADO SON LOS SIGUIENTES: \n', script.calls)
        end = time.time()
        print("---------")
        print('Execution time:', end-start, 'seconds.')
        print('-----------------------------------------------------------------------------------------------------\n')
    elif len(sys.argv) >= 2:
        if name.endswith('.py'):
            print("***************************************\n")
            print("***Estamos trabajando con DISCERN2.***\n")
            print("***************************************\n")

            ls = sys.argv[2:]
            for i in range(len(ls)):
                ls[i] = os.path.abspath(ls[i])
            script = Discern2(name, ls)
            #saveast()      
            #script.yieldfind()
            '''
            print('-----------------------------------------------------------------------------------------------------\n')
            print('In the following list we find the node\'s namespace of the generators defined in the script of interest:')
            for i in range(len(script.generators)):
                print('\n', i, ': \n', script.generators[i])
            print("----------")
            '''
            #script._generatorfind()
            '''
            print('In the following list we find the namespace of the generators defined in the script of interest:')
            for i in range(len(script.generators)):
                print('\n', i, ': \n', script.generators[i])
            print("----------")
            '''

            folder = sys.argv[1]   
            info = [0,0] # empty, no empty
            imports_ini = []
            all_ini = []
            body = []
            body_all = []

            some_dir = folder.rstrip(os.path.sep)
            num_sep = some_dir.count(os.path.sep)

            for i in os.walk(folder):
                dirpath, dirname, filnames = i[0], i[1], i[2]
    
                for s_file in filnames:
                    level = abs(num_sep-dirpath.count(os.path.sep))
                    fullpath = os.path.join(dirpath, s_file)
                    if s_file.endswith('.py'):
                        if s_file == '__init__.py' and os.path.getsize(fullpath) == 0:
                            info[0] += 1
                        elif s_file == '__init__.py' and os.path.getsize(fullpath) != 0:
                            info[1] += 1
                            content = _reader(fullpath)
                            imports_ini = _management_imports(content, level, dirpath.rstrip(os.path.sep))
                            all_ini.insert(0, imports_ini)
                        else:
                            content = _reader(fullpath)
                            body = _management_files(content, imports_ini, level)
                            body_all.append(body)
            
            all_ini = list(filter(None, all_ini))
            print(info)
            #_save_only(all_ini)
            _save_only(body_all)

            script.assign_call_find()
            print('LOS ASSIGNS SON LOS SIGUIENTES: ', script.assigns)
            print('LOS GENERATORS SON LOS SIGUIENTES: ', script.generators)
            print('LOS CALLS QUE HEMOS ENCONTRADO SON LOS SIGUIENTES: \n', script.calls)
            end = time.time()
            print("---------")
            print('Execution time:', end-start, 'seconds.')
            print('---------------------------------------------------------------------------------------------\n')
        else: 
            #TO DO  in this case we're in a folder. We need to make a 'FolderCalls' class for Discern2
            pass




if __name__ == '__main__':
    main(sys.argv[1])
