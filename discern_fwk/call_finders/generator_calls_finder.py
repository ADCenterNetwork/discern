import ast
from discern_fwk.pattern_finders.generator_finder_utils import GeneratorFinderUtils
from typing import List
from discern_fwk.call_finders.result_types.calls_search_result import CallsSearchResult
from discern_fwk.call_finders.abstract_calls_finder import AbstractCallsFinder

class GeneratorCallsFinder(AbstractCallsFinder):

    def __init__(self, pattern_finder):
        self.pattern_finder = pattern_finder
        self.calls = {}
        self.assigns = {}

    def findPatternCalls(self) -> CallsSearchResult:
        '''
            This is the main entry point of the algorithm to find the pattern calls.
        '''
        # initialization
        soft_project = self.pattern_finder.get_software_project()
        self.assigns = {}
        call_search_result = CallsSearchResult()
        if (soft_project.hasMainFile()):
            mainFile = soft_project.getMainFile()
            self.calls = {}
            tree = mainFile.getNodeForFile()
            self.pattern_finder._generatorfind(tree)
            generators = self.pattern_finder.get_generators()

            call_search_result.setPatternCallsForFile(mainFile.getFullPath(), self.assign_call_find(tree, generators))
        else:
            for file in soft_project.getFilesGenerator():
                self.calls = {}
                if file.fileName != '__init__.py':
                    tree = file.getNodeForFile()
                    self.pattern_finder._generatorfind(tree)
                    generators = self.pattern_finder.get_generators()
                    # folderCalls[file.fileName] = self.assign_call_find(tree, generators)
                    call_search_result.setPatternCallsForFile(file.getFullPath(), self.assign_call_find(tree, generators))
        return call_search_result

    def assign_call_find(self, node, generators):
        """assign_call_find is an idea to search the call to new assignments at the moment they are assigned
         and it still is in development.

        Args:
            node ([ast object], optional): [We node we are working in. The idea is to start at the Module node
            and walk up the tree branches.]. Defaults to None.
        """
        # self._generatorfind(node)
        for child in ast.iter_child_nodes(node):
            if generators == []:
                break
            elif isinstance(child, ast.Assign):
                self.new_variable = child
                self._assignsearch(child, generators)
                # Check for calls to generators in the same node
                self.assign_call_find(child, generators)
            elif isinstance(child, ast.Call):
                # This _findcall only detects call to our generator list.
                self._findcall(child, generators)
            else:
                # Else call recursively
                self.assign_call_find(child, generators)

        return self.calls

    def _assignsearch(self, node, generators):
        """_assignsearch is a function that will search along the namespace of 'generators' and will call to __assignfind
        in order to find if that element has been assigned as a new variable.

        Args:
            node ([ast object], optional): [We node we are working in.]
        """
        for s in range(len(generators)):
            self.__assignfind(node, node, generators[s][:], 0)
            nodeName = GeneratorFinderUtils.get_name(node)
            if nodeName in self.assigns.keys() and self.assigns[nodeName] in generators:
                break

    def __assignfind(self, new_variable, node, ls, i):
        """__assignfind will travel the branches of the tree
            in order to detect assignments to our element of interest
            in the namespace of 'generators'.
        Args:
            node ([ast object], optional): [We node we are working in.]
            sublista([list]): [We are searching assignments of our generators in every node. In sublista we record
            the generator namespace.]
        """

        # 'node' is an assign variable, and 'ls', the list we're working on
        for child in ast.iter_child_nodes(node):
            if child.__class__.__name__ == 'Call':
                if GeneratorFinderUtils.get_name(child) in ls:
                    self.__check_assign_is_correct(child, ls, new_variable)
            elif child.__class__.__name__ == 'Name':
                self.__check_previous_assign(node, child)
            elif child.__class__.__name__ == 'Tuple':
                self.__check_multiple_assign(node, ls)
            else:
                self.__assignfind(new_variable, child, ls, i)

    def __check_multiple_assign(self, node, ls):
        try:  # We put a try/except for cases a,b = function_that_returns_two_objects. We have to include this case.
            for j in range(len(node.value.elts)):
                self.__assignfind_multiple(node.targets[0].elts[j], node.value.elts[j], ls)
        except AttributeError:
            pass

    def __check_assign_is_correct(self, child, ls, new_variable):
        if ast.iter_child_nodes(child):
            for childchild in ast.walk(child):
                if GeneratorFinderUtils.get_name(childchild) in ls or GeneratorFinderUtils.get_name(childchild) in self.assigns:  # and childchild != child:
                    if childchild != child:
                        i = ls.index(GeneratorFinderUtils.get_name(child))
                        self.assigns[GeneratorFinderUtils.get_name(new_variable)] = [GeneratorFinderUtils.get_name(child)]
                        self.___assignfind(new_variable, child, ls, i-1)
        else:
            i = ls.index(GeneratorFinderUtils.get_name(child))
            self.assigns[GeneratorFinderUtils.get_name(new_variable)] = [GeneratorFinderUtils.get_name(child)]
            self.___assignfind(new_variable, child, ls, i-1)

    def __check_previous_assign(self, node, child):
        if GeneratorFinderUtils.get_name(child) in self.assigns.keys():
            try:
                self.assigns[node.targets[0].id] = self.assigns[GeneratorFinderUtils.get_name(child)]
            except:  # Do not remove this except pass. It stop working well.
                pass

    def __assignfind_multiple(self, left_side, right_side, ls):

        if right_side.__class__.__name__ == 'Call':
            if GeneratorFinderUtils.get_name(right_side) in ls:
                i = ls.index(GeneratorFinderUtils.get_name(right_side))
                self.assigns[GeneratorFinderUtils.get_name(left_side)] = [GeneratorFinderUtils.get_name(right_side)]
                self.___assignfind(left_side, right_side, ls, i-1)

        if right_side.__class__.__name__ == 'Name':
            if GeneratorFinderUtils.get_name(right_side) in self.assigns.keys():
                self.assigns[GeneratorFinderUtils.get_name(left_side)] = self.assigns[GeneratorFinderUtils.get_name(right_side)]

    def ___assignfind(self, new_variable, node, ls, i):
        '''we want to check if any of the descendants of 'node' is in our list ls in the index i'''
        for child in ast.iter_child_nodes(node):
            if child.__class__.__name__ == 'Call':
                i = self.__save_assign_and_return_i(child, new_variable, ls, i)

            elif child.__class__.__name__ == 'Name':
                if GeneratorFinderUtils.get_name(child) in self.assigns.keys():
                    for item in self.assigns[GeneratorFinderUtils.get_name(child)]:
                        i = len(self.assigns[GeneratorFinderUtils.get_name(child)]) - 1
                        self.assigns[GeneratorFinderUtils.get_name(new_variable)].insert(0, item)
                else:
                    self.___assignfind(new_variable, child, ls, i)
            self.___assignfind(new_variable, child, ls, i)

    def __save_assign_and_return_i(self, child, new_variable, ls, i):
        if GeneratorFinderUtils.get_name(child) == ls[i]:
            self.assigns[GeneratorFinderUtils.get_name(new_variable)].insert(0, GeneratorFinderUtils.get_name(child))
            i = i-1
        else:
            try:
                del self.assigns[GeneratorFinderUtils.get_name(new_variable)]
            except:  # Do not remove this except pass. It stop working well.
                pass
        return i

    def _findcall(self, node, generators):
        '''
            Finds calls to the generator list generators, 
            and saves them into the self.calls collection.
            Internally, it uses the self.self_dictionary to know the types of the processed nodes.
        '''
        current_calls = self.calls.copy()
        calls_temp = self.calls.copy()
        prov_calls = []
        for generator in generators:
            self.__findcall(node, generator, len(generator)-1, self.assigns, current_calls)
            if current_calls != calls_temp:
                prov_calls.append(generator)
                calls_temp = current_calls.copy()

        self.__filter_incorrect_calls_same_line(node, prov_calls, calls_temp)
        # last, save the calculated list into self.calls
        self.calls = calls_temp

    def __filter_incorrect_calls_same_line(self, node, prov_calls, calls):
        if len(prov_calls) >= 2:
            len_pv = list(map(lambda x: len(x), prov_calls))
            max_item = max(len_pv, key=int)
            max_item_index = len_pv.index(max_item)
            correct_gen = prov_calls[max_item_index]
            for sublista in prov_calls:
                if sublista != correct_gen and tuple(sublista) in calls:
                    calls[tuple(sublista)].remove(node.lineno)
                    if len(calls[tuple(sublista)]) == 0:
                        # if the list is empty, remove the key
                        del calls[tuple(sublista)]

    def __findcall(self, node, ls, i, assigns, calls):
        if node.__class__.__name__ == 'Call':
            i = self.__check_call_and_return_i(node, ls, i, assigns, calls)
        elif node.__class__.__name__ == 'Name':
            # We will enter here when we do not have a 'call', to check if it's an assigned variable
            if GeneratorFinderUtils.get_name(node) in self.assigns:
                self.__check_call_to_assign(node, ls, i, assigns, calls)
            elif GeneratorFinderUtils.get_name(node) == ls[i]:
                self.___findcall(node, ls, i, assigns, calls)
            elif node.id == 'self':
                self.__check_class(node, ls, i, assigns, calls)
        elif node.__class__.__name__ == 'Attribute' and node.value.__class__.__name__ == 'Attribute':
            if node.value.attr == ls[i]:
                self.___findcall(node.value, ls, i, assigns, calls)
        else:
            for child in ast.iter_child_nodes(node):
                self.__findcall(child, ls, i, assigns, calls)

    def __check_class(self, node, ls, i, assigns, calls):
        if node in self.self_dictionary.keys():
            if self.self_dictionary[node] == ls[i]:
                self.___findcall(node, ls, i, assigns, calls)

    def __check_call_to_assign(self, node, ls, i, assigns, calls):
        i = i - len(assigns[GeneratorFinderUtils.get_name(node)])
        original_variables = assigns[GeneratorFinderUtils.get_name(node)]
        if set(original_variables).issubset(ls):
            self.___findcall(node, ls, i, assigns, calls)

    def __check_call_and_return_i(self, node, ls, i, assigns, calls):
        if GeneratorFinderUtils.get_name(node) == ls[i]:
            self.___findcall(node, ls, i, assigns, calls)
        else:
            for child in ast.iter_child_nodes(node):
                self.__findcall(child, ls, i, assigns, calls)
        return i

    def ___findcall(self, node, ls, i, assigns, calls):
        '''we create this function to simplify '__findcall' and add the list to our
        dictionary of calls if we're in index 0, or continue
        in __findcall otherwise'''
        if i <= 0:  # If this is the case, we want to add this list as a call
            self.__save_call(node, ls, calls)
        else:  # Otherwise, we want to continue the same process with its children
            for child in ast.iter_child_nodes(node):
                self.__findcall(child, ls, i-1, assigns, calls)

    def __save_call(self, node, ls, calls):
        '''
            Adds the line number of the node to the namespace to the "calls" collection
            or creates the first element accordingly.
        '''
        if tuple(ls) in calls.keys():
            if not node.lineno in calls[tuple(ls)]:
                calls[tuple(ls)].append(node.lineno)
        else:
            calls[tuple(ls)] = [node.lineno]

        return calls
