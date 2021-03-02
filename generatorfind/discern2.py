import ast, os
from ast2json import ast2json
from io import open
from setuptools import setup
from .generatorfind import self_finder
from .generatorfind import get_folder
from .generatorfind import get_name


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
            name:: string = The name of the file that we are obtaining information from,
                             when we execute method _generatorfind()
            ls_modules:: [string] = Modules to take into account in the algorithm
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
        # Iterate over nodes assigning an id to each one
        for node in ast.walk(self.tree):
            self.id[node] = i
            i += 1

    def sourcemapyield(self, node=None, ls=[]):
        if node is None:
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

    def __yieldfind(self, node=None, ls=[]):
        """Yieldfind search 'Yield's nodes and walk up the tree branch, saving all the nodes 
        that contain that generator.

        Args:
            node ([ast object], optional): [A node through which we will travel to find the yield child node. 
            At first, we will input the module object]. Defaults to None.
            ls (list, optional): [List that we record the nodes we travel until find the yield node.]. Defaults to [].
        """
        if node is None:
            node = self.tree

        # If the node type is IMPORT we will parse that imported file and we will search generators on that file.
        if node.__class__.__name__ == 'Import':
            self.__register_generator_of_import_file(node, ls)

        # If the node type is IMPORTFROM we will parse that imported file and we will search generators on that file.
        if node.__class__.__name__ == 'ImportFrom':
            self.__register_generator_of_importfrom_file(node, ls)

        # Yield node found, base case of recursion.
        if node.__class__.__name__ == 'Yield':
            self.__register_generator(node, ls)

        # We continue iterating until find a node of interest.
        else:
            if ast.iter_child_nodes(node):
                self.__iterate_over_child_nodes(node, ls)

        return self.generators

    def __register_generator_of_import_file(self, node, ls):
        # We make a loop because we can import multiples files on a time.
        for i in range(len(node.names)):
            # We construct the path of the file imported in order to parse it.
            importpath = node.names[i].name.split('.')
            absolute_path = os.path.join(os.getcwd(), self.__fullpath_imported_file(node, ls, importpath))
            if self.__imported_file_correct(node, ls, importpath, absolute_path):
                # In this case, we have imported a file that has generators inside. So, we parse it and search generators.
                self.__parse_and_register_gen(node, ls, importpath, i)
            elif absolute_path in self.modules:  # We are in a folder. We have to modify:
                self.__check_import_alias(node, ls, importpath, i)
                # Calls to find yield commands in folders
                self.__yieldfind_folders(absolute_path, ls)

    def __parse_and_register_gen(self, node, ls, importpath, i):
        self.__check_import_alias(node, ls, importpath, i) #We check the asname (if exists) in order to register namespace.
        fileimp = self.__fullpath_imported_file(node, ls, importpath)+'.py'
        # Parse fileimp with AST library
        treeimp = ast.parse(open(fileimp, encoding="iso-8859-15", errors='ignore').read())
        # Recursive call in order to find  yield nodes in the imported file.
        self.__yieldfind(treeimp, ls)
        # We remove redundant elements.
        [ls.pop(0) for n in range(len(importpath)+1)]

    def __check_import_alias(self, node, ls, importpath, i):
        if node.names[i].asname:
            ls.append(node.names[i].asname)
        else:
            for item in importpath:
                ls.append(item)

    def __imported_file_correct(self, node, ls, importpath, absolute_path):
        return (os.path.isfile(self.__fullpath_imported_file(node, ls, importpath)+'.py')  and (absolute_path+'.py' in self.modules))

    def __fullpath_imported_file(self, node, ls, importpath):
        fullpath = get_folder(self.path)
        for j in range(len(importpath)):
            fullpath = os.path.join(fullpath, importpath[j])
        return fullpath

    def __register_generator_of_importfrom_file(self, node, ls):
        '''In a node like this one, the attribute 'module' contains the name of the left side (from left_side
        import right_side), in the same way it's represented in code (separated by dots)

        And the attribute node.names will return a list, where each element is an 'Alias' and it represents
        the element we're importing, i.e, the right_side. To get its name we apply the attribute '.name', 

        If there is a python file, we know this either has to be on the last element of the left_side, or it 
        will be on the right side
        '''
        getfolder = get_folder(self.path).split('/')
        if node.module is None:  # The importfrom has the structure: "from . import file".
            full_path = self.__construct_import_path_without_left_side(node, getfolder)
            filename = full_path+'.py'
        else:  # The importfrom has the structure "from .folder import filde".
            full_path = self.__construct_import_path_with_left_side(node, getfolder)
            filename = full_path + '.py'

        if self.__importfrom_file_correct(filename):  # The imported file was on left_side, so we can parse it.
            tree2 = ast.parse(open(filename, encoding="iso-8859-15", errors='ignore').read())
            self.__yieldfind(tree2, ls)  # Recursive call to yielfind.
        else:  # In this case, it means we have to access the right_side and look for files.
            self.__construct_path_with_right_side(node, full_path, ls)

    def __construct_path_with_right_side(self, node, full_path, ls):
        right_side = node.names
        for alias in right_side:
            alias_filename = alias.name + '.py'
            filename_path = os.path.join(full_path, alias_filename)
            if self.__importfrom_file_correct(filename_path):
                # We append the alias to get the correct namespace.
                ls.append(alias)
                tree2 = ast.parse(open(filename_path, encoding="iso-8859-15", errors='ignore').read())
                # Recursive call.
                self.__yieldfind(tree2, ls)

    def __importfrom_file_correct(self, filename):
        return os.path.isfile(filename) and (filename in self.modules)

    def __construct_import_path_with_left_side(self, node, getfolder):
        left_side = node.module.split('.')
        # We now form a path from the elements on the left_side
        full_path2 = self.__separate_path_elements(node, getfolder)
        self.__check_relative_level(node, full_path2)
        full_path = full_path2[0]
        full_path2.pop(0)
        variable = 0
        # We have the path o a list, so on next line we join the elements of the lists with the os library. 
        for item in full_path2:
            if not variable == 0:
                full_path = os.path.join(full_path, item)
            else:
                full_path = os.path.join(full_path + os.sep, item)
                variable += 1
        for item in left_side:
            full_path = os.path.join(full_path, item)
        return full_path

    def __construct_import_path_without_left_side(self, node, getfolder):
        full_path2 = self.__separate_path_elements(node, getfolder)
        self.__check_relative_level(node, full_path2)
        full_path = full_path2[0]
        full_path2.pop(0)
        variable = 0
        for item in full_path2:
            if not variable == 0:
                full_path = os.path.join(full_path, item)
            else:
                full_path = os.path.join(full_path + os.sep, item)
                variable += 1
        return full_path

    def __check_relative_level(self, node, full_path2):
        if node.level > 0:
            for i in range(node.level-1):
                full_path2.pop(-1)

    def __separate_path_elements(self, node, getfolder):
        full_path2 = os.getcwd()
        for item in getfolder:
            full_path2 = os.path.join(full_path2, item)
        full_path2 = full_path2.split('\\')
        return full_path2

    def __register_generator(self, node, ls):
        ls.append(node)
        x = ls[:]
        self.generators.append(x)

    def __iterate_over_child_nodes(self, node, ls):
        ls.append(node)
        for child in ast.iter_child_nodes(node):
            y = ls[:]
            # Recursive call
            self.__yieldfind(child, y)

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
        """_generatorfind() : works with our list 'generators' in order to
        obtain the correct namespace instead of all the nodes information.
        """
        self.generators = []  # Restart generator's list.
        self.generators = self.__yieldfind()

        # Iterates over the generated matrix
        for i in range(len(self.generators)):
            k = 0
            for j in range(len(self.generators[i])-1):
                if self.generators[i][-j-1].__class__.__name__ == "FunctionDef":
                    self.generators[i] = self.generators[i][1:-j]
                    break
            for m in range(len(self.generators[i])):
                j = -m - 1
                # If the node has name, we record it.
                if self.__node_with_name(self.generators[i][j]):
                    if not type(self.generators[i][j]) == str:
                        self.generators[i][j] = self.generators[i][j].name
                elif self.generators[i][j].__class__.__name__ == 'Module':
                    k += 1
                elif self.generators[i][j].__class__.__name__ == 'Import':
                    self.__record_import_name(i, j, k)
                elif self.generators[i][j].__class__.__name__ == 'ImportFrom':
                    self.__record_importfrom_name(i, j, k)
                elif self.generators[i][j].__class__.__name__ == 'If':
                    pass
                elif self.generators[i][j].__class__.__name__ == 'For':
                    pass
                elif self.generators[i][j].__class__.__name__ == 'Try':
                    pass
            self.__clean_namespace(i)

        self.__remove_repeated_elements()
        return self.generators

    def __remove_repeated_elements(self):
        aux = []
        for ls in self.generators:
            if ls not in aux:
                aux.append(ls)
        self.generators = aux[:]

    def __clean_namespace(self, i):
        self.generators[i] = [item for item in self.generators[i] if item.__class__.__name__ != 'Module']
        self.generators[i] = [item for item in self.generators[i] if item.__class__.__name__ != 'If']
        self.generators[i] = [item for item in self.generators[i] if item.__class__.__name__ != 'For']
        self.generators[i] = [item for item in self.generators[i] if item.__class__.__name__ != 'Try']

    def __record_importfrom_name(self, i, j, k):
        if self.generators[i][j].names[k-1].asname:
            self.generators[i][j] = self.generators[i][j].names[k-1].asname
        elif self.generators[i][j].names[k-1].name:
            self.generators[i][j] = self.generators[i][j].names[k-1].name

    def __record_import_name(self, i, j, k):
        if self.generators[i][j].names[k-1].asname:
            self.generators[i][j] = self.generators[i][j].names[k-1].asname
        else:
            self.generators[i][j] = self.generators[i][j].names[k-1].name

    def __node_with_name(self, node):
        return (not node.__class__.__name__ == 'Import' and not node.__class__.__name__ == 'Module' and not node.__class__.__name__ == 'If' and not node.__class__.__name__ == 'For' and not node.__class__.__name__ == 'If' and not node.__class__.__name__ == 'Try')

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
