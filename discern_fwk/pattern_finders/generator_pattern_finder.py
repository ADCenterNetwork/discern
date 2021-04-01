import ast
from discern_fwk.call_finders.generator_calls_finder import GeneratorCallsFinder
import os
import io
from discern_fwk.pattern_finders.generator_finder_utils import GeneratorFinderUtils
from typing import Dict, List, Tuple
from discern_fwk.pattern_finders.result_types.pattern_search_result import PatternSearchResult
from discern_fwk.pattern_finders.result_types.generator_search_result import GeneratorSearchResult
from discern_fwk.pattern_finders.abstract_pattern_finder import AbstractPatternFinder

class GeneratorPatternFinder(AbstractPatternFinder):

    def __init__(self, softwareProject):
        """We define some variables that are essential in the process of obtaining information and other variables # noqa: E501
        that will store the information of interest.

        Args:
            name:: string = The name of the file that we are obtaining information from, # noqa: E501
                             when we execute method _generatorfind()
            ls_modules:: [string] = Modules to take into account in the algorithm # noqa: E501
        """
        # Save software project object and its path
        self.soft_project = softwareProject
        self.path = softwareProject.getProjectPath()
        self.tree = None
        self.generators = []
        self.new_variable = None
        self.temporalassign = {}
        self.self_dictionary = {}
        self.print = []
        self.sourcemap = {}
        self.id = {}  # dictionary with key=NODE and value=INT_ID
        self.yieldsdict = {}
        self.yieldslist = []

    def findPatterns(self) -> List[PatternSearchResult]:
        results = []
        self.compute_modules_with_generators()
        if (self.soft_project.hasMainFile()):
            mainFile = self.soft_project.getMainFile()
            self.__find_generators_for_file(mainFile, results)
        else:
            for file in self.soft_project.getFilesGenerator():
                self.__find_generators_for_file(file, results)

        return results

    def findCalls(self):
        # Create the call finder with a reference to the pattern finder
        calls_finder = GeneratorCallsFinder(self)
        self.compute_modules_with_generators()
        return calls_finder.findPatternCalls()

    def get_software_project(self):
        return self.soft_project

    def get_generators(self):
        return self.generators

    def compute_modules_with_generators(self) -> List[str]:
        self.modules = []
        for file in self.soft_project.getFilesGenerator():
            if file.fileName == '__init__.py':
                path = file.getFullPath().split('\\')
                path.pop(-1)
                folderpath = path[0]+'\\'
                path.pop(0)
                for j in range(len(path)):
                    folderpath = os.path.join(folderpath, path[j])
                self.modules.append(folderpath)
            tree = file.getNodeForFile()
            if self._generatorfind(tree) != []:
                self.modules.append(file.getFullPath())

        return self.modules

    def __find_generators_for_file(self, file, results):
        tree = file.getNodeForFile()
        self._generatorfind(tree)
        for generator in self.generators:
            results.append(GeneratorSearchResult(generator))

    def sourcemapyield(self, node=None, ls=[]):
        if node is None:
            node = self.tree
        if node.__class__.__name__ == 'Yield':
            ls.append(node)
            # x = ls[:]
            self.yieldslist.append(node)
        else:
            if ast.iter_child_nodes(node):
                for child in ast.iter_child_nodes(node):
                    y = ls[:]
                    self.sourcemapyield(child, y)

        for nodoyield in self.yieldslist:
            self.yieldsdict[self.id[nodoyield]] = {"id": self.id[nodoyield],
                                                   "col_offset": nodoyield.col_offset,
                                                   "lineno": nodoyield.lineno}
        return self.yieldsdict

    def __yieldfind(self, node, ls=[]):
        """Yieldfind search 'Yield's nodes and walk up the tree branch, saving all the nodes
        that contain that generator.

        Args:
            node ([ast object], optional): [A node through which we will travel to find the yield child node.
            At first, we will input the module object]. Defaults to None.
            ls (list, optional): [List that we record the nodes we travel until find the yield node.]. Defaults to [].
        """
        # if node is None:
        #     node = self.tree

        # If the node type is IMPORT we will parse that imported file
        # and we will search generators on that file.
        if node.__class__.__name__ == 'Import':
            self.__register_generator_of_import_file(node, ls)

        # If the node type is IMPORTFROM we will parse that imported file
        # and we will search generators on that file.
        elif node.__class__.__name__ == 'ImportFrom':
            self.__register_generator_of_importfrom_file(node, ls)

        # Yield node found, base case of recursion.
        elif node.__class__.__name__ == 'Yield':
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
            absolute_path = os.path.join(self.path,
                                         self.__fullpath_imported_file(node, ls, importpath))
            if self.__imported_file_correct(node,
                                            ls, importpath,
                                            absolute_path):
                # In this case, we have imported a file that has
                # generators inside. So, we parse it and search generators.
                self.__parse_and_register_gen(node, ls, importpath, i)
            elif absolute_path in self.modules:  # We are in a folder
                # We have to modify:
                self.__check_import_alias(node, ls, importpath, i)
                # Calls to find yield commands in folders
                self.__yieldfind_folders(absolute_path, ls)

    def __parse_and_register_gen(self, node, ls, importpath, i):
        # We check the asname (if exists) in order to register namespace.
        self.__check_import_alias(node, ls, importpath, i)
        fileimp = self.__fullpath_imported_file(node, ls, importpath)+'.py'
        # Parse fileimp with AST library
        treeimp = ast.parse(io.open(fileimp,
                                    encoding="iso-8859-15",
                                    errors='ignore').read())
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
        absolute_path2 = os.path.abspath(absolute_path+'.py')
        return (os.path.isfile(self.__fullpath_imported_file(node, ls, importpath)+'.py') and (absolute_path2 in self.modules))

    def __fullpath_imported_file(self, node, ls, importpath):
        fullpath = self.path
        for j in range(len(importpath)):
            fullpath = os.path.join(fullpath, importpath[j])
        return fullpath

    def __register_generator_of_importfrom_file(self, node, ls):
        '''In a node like this one, the attribute 'module' contains
           the name of the left side (from left_side import right_side),
           in the same way it's represented in code (separated by dots)

           And the attribute node.names will return a list, where each
           element is an 'Alias' and it represents the element
           we're importing, i.e, the right_side.
           To get its name we apply the attribute '.name':
           If there is a python file, we know this either has to be on
           the last element of the left_side, or it
           will be on the right side
        '''
        getfolder = self.path.split('/')
        if node.module is None:  # The importfrom has the structure: "from . import file".
            full_path = self.__construct_import_path_without_left_side(node, getfolder)
            filename = full_path+'.py'
        else:  # The importfrom has the structure "from .folder import file".
            full_path = self.__construct_import_path_with_left_side(node, getfolder)
            filename = full_path + '.py'

        if self.__importfrom_file_correct(filename):  # The imported file was on left_side, so we can parse it.
            tree2 = ast.parse(io.open(filename, encoding="iso-8859-15", errors='ignore').read())
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
                tree2 = ast.parse(io.open(filename_path, encoding="iso-8859-15", errors='ignore').read())
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
            if variable > 0:
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
            for i in range(node.level-2):
                full_path2.pop(-1)

    def __separate_path_elements(self, node, getfolder):
        #full_path2 = os.getcwd()
        full_path2 = self.path
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
            init_tree = ast.parse(io.open(init_filename, encoding="iso-8859-15", errors='ignore').read())
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
                        tree2 = ast.parse(io.open(filename, encoding="iso-8859-15", errors='ignore').read())
                        self.__yieldfind(tree2, ls)

    def _generatorfind(self, tree):
        """_generatorfind() : works with our list 'generators' in order to
        obtain the correct namespace instead of all the nodes information.
        """
        self.tree = tree
        self.self_dictionary = GeneratorFinderUtils.self_finder(tree, '', {})
        self.generators = []  # Restart generator's list.
        self.generators = self.__yieldfind(tree)

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
