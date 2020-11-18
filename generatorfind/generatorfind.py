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
    full_path = os.path.join(os.getcwd(), path)
    return full_path

class Code():
    """Code is a class that contains all the functions involved in the work with the ast of the file of interest.
    """
    def __init__(self, name):
        """we define some variables that are essential in the process of obtaining information and other variables 
        that will store the information of interest.

        Args:
            name ([string]): [The name of the file that we are obtaining information when we execute generatorfind.py ]
        """
        self.tree = ast.parse(open(name).read())
        self.generators = []
        self.path = name
        self.calls = {}
        self.assigns = {}
        self.called = []
    
    def yieldfind(self, node = None, ls = []):
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
            ls.append(node)
            for i in range(len(node.names)):
                folder = _get_folder(self.path)
                imported_file = os.path.join(folder, node.names[i].name+'.py')
                tree2 = ast.parse(open(imported_file).read())
                self.yieldfind(tree2, ls)
        if node.__class__.__name__ == 'Yield':
                ls.append(node)
                x = ls[:]
                self.generators.append(x)
        else:
                if ast.iter_child_nodes(node):
                    ls.append(node)
                    for child in ast.iter_child_nodes(node):
                        y = ls[:]
                        self.yieldfind(child, y)

    def generatorfind(self):
        """generatorfind works with our list 'generators' in order to obtain the correct namespace instead of all the
        nodes information.
        """
        nodes=self.generators[:]
        for i in range(len(self.generators)):
            k = 0
            for j in range(len(self.generators[i])-1): 
                if  self.generators[i][-j-1].__class__.__name__ == "FunctionDef" :
                    self.generators[i] = self.generators[i][1:-j]
                    break
            for m in range(len(self.generators[i])):
                j = -m - 1
                if not self.generators[i][j].__class__.__name__ =='Import' and not self.generators[i][j].__class__.__name__ =='Module':
                    self.generators[i][j] = self.generators[i][j].name
                elif self.generators[i][j].__class__.__name__ == 'Module':
                    k +=1
                elif self.generators[i][j].__class__.__name__ =='Import':
                    if self.generators[i][j].names[k-1].asname:
                        self.generators[i][j] = self.generators[i][j].names[k-1].asname
                    else:
                        self.generators[i][j] = self.generators[i][j].names[k-1].name
            self.generators[i] = [item for item in self.generators[i] if item.__class__.__name__ != 'Module']

            
    def assign_call_find(self, node = None):
        """assign_call_find is an idea to search the call to new assignments at the moment they are assigned
         and it still is in development.

        Args:
            node ([ast object], optional): [We node we are working in. The idea is to start at the Module node
            and walk up the tree branches.]. Defaults to None.
        """
        if node == None:
            node = self.tree
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.Assign):
                self.assignsearch(child)
            if isinstance(child, ast.Call) or isinstance(child, ast.Name) or isinstance(child, ast.Attribute):
                #TO DO
                self.findcall(child) #This findcall only detects call to our generator list.
                                     #We still have to develop an analogous function to detect calls to assigns.
                pass
            self.assign_call_find(child)


      
    def assignsearch(self, node):
        """assignsearch is a function that will search along the namespace of 'generators' and will call to __assignfind
        in order to find if that element has been assigned as a new variable.

        Args:
            node ([ast object], optional): [We node we are working in.]
        """
        for s in range(len(self.generators)):
            self.__assignfind(node,  self.generators[s][:])
        
        #print(self.assigns)

    def __assignfind(self, node, sublista):
        """__assignfind will travel the branches of the tree in order to detect assignments to our element of interest
        in the namespace of 'generators'.


        Args:
            node ([ast object], optional): [We node we are working in.]
            sublista([list]): [We are searching assignments of our generators in every node. In sublista we record
            the generator namespace.]
        """
        for child in ast.walk(node):
            if isinstance(child,  ast.Call):
                if get_name(child) in sublista: # self.generators[s][:]
                    for j in range(len(sublista)):
                        if sublista[j] == get_name(child):
                            self.assigns[node.targets[0].id] = sublista[0:j+1]
                            break

    def findcall(self, node):
        """findcall will walk up the tree searching the calls to our different generators, and will allow us to record
        some information about the call node, as for example the line of the call.

        Args:
            node ([ast object], optional): [We node we are working in.]
        """
        for child in ast.walk(node):
            if child.__class__.__name__ == 'Call':
                for ls in self.generators:
                    if get_name(child) == ls[0]:
                        if len(ls) > 1:
                            self.findcall2(child, ls, child.lineno, self.called)
                        else:
                            x = [get_name(child), child.lineno]
                            if not x in self.called:
                                try:
                                    self.calls[tuple(ls)].append(child.lineno)
                                except KeyError:
                                    self.calls[tuple(ls)] = [child.lineno]
                                self.called.append(x)
                                print('Hemos encontrado el call de ', ls, ' en la linea ', child.lineno)
            elif child.__class__.__name__ == 'Name':
                for ls in self.generators:
                    if child.id == ls[0]:
                        if len(ls) > 1:
                            self.findcall2(child, ls, child.lineno, self.called)
                        else:
                            x = [child.id , child.lineno]
                            if not x in self.called:
                                try:
                                    self.calls[tuple(ls)].append(child.lineno)
                                except KeyError:
                                    self.calls[tuple(ls)] = [child.lineno]
                                self.called.append(x)
                                print('Hemos encontrado el call de ', ls, ' en la linea ', child.lineno)
            
            elif child.__class__.__name__ == 'Attribute':
                for ls in self.generators:
                    if child.value == ls[0]:
                        if len(ls) > 1:
                            self.findcall2(child, ls, child.lineno, self.called)
                        else:
                            x = [child.value, child.lineno]
                            if not x in self.called:
                                try:
                                    self.calls[tuple(ls)].append(child.lineno)
                                except KeyError:
                                    self.calls[tuple(ls)] = [child.lineno]
                                self.called.append(x)
                                print('Hemos encontrado el call de ', ls, ' en la linea ', child.lineno, self.called)

    def findcall2(self, child, ls, lineno, called, i = 0):
        """findcall2 is an internal function of findcall that help us to search calls to our generators when 
        the namespace of our generator has more than one element.

        Args:
            child ([ast object]): [Node in which we are working. Its name is child because we are walking up the 
            tree along the child nodes.]
            ls ([list]): [A nested list with the namespace of a generator.]
            lineno ([int]): [number of line where the call is located.]
            called ([list]): [Our search method gives us repeated values of calls, so with this list we control
            that we do not have unnecessary information. THIS METHOD MAY BE IMPROVED TO AVOID THIS.]
            i (int, optional): [index of our element of interest in generators list]. Defaults to 0.
        """
        #for child in ast.walk(node):
        if child.__class__.__name__ == 'Call' and child.lineno==lineno: #and get_name(child) == ls[i+1] and child.lineno == lineno:
            if i+1 == len(ls) -1:
                x = [ls, lineno]
                if not x in self.called:
                    try:
                            self.calls[tuple(ls)].append(child.lineno)
                    except KeyError:
                            self.calls[tuple(ls)] = [child.lineno]
                    self.called.append(x)
                    print('Hemos encontrado el call de ', ls, ' en la linea ', child.lineno)
            else:
                self.findcall2(child, ls, child.lineno, self.called, i+1)
        elif child.__class__.__name__ == 'Name' and child.lineno == lineno:#child.id == ls[i+1] and child.lineno == lineno:
            if i+1 == len(ls) -1:
                x = [ls, lineno]
                if not x in self.called:
                    try:
                            self.calls[tuple(ls)].append(child.lineno)
                    except KeyError:
                            self.calls[tuple(ls)] = [child.lineno]
                    self.called.append(x)
                    print('Hemos encontrado el call de ', ls, ' en la linea ', child.lineno)
            else:
                self.findcall2(child, ls, child.lineno, self.called, i+1)
        elif child.__class__.__name__ == 'Attribute' and child.lineno==lineno:#child.value == ls[i+1] and child.lineno == lineno:
            if i+1 == len(ls) -1:
                x = [ls, lineno]
                if not x in self.called:
                    try:
                        self.calls[tuple(ls)].append(child.lineno)
                    except KeyError:
                        self.calls[tuple(ls)] = [child.lineno]
                    self.called.append(x)
                    print('Hemos encontrado el call de ', ls, ' en la linea ', child.lineno)
            else:
                self.findcall2(child, ls, child.lineno, self.called, i+1)




def main(name):
    start = time.time()
    script = Code(name)
    saveast()      
    script.yieldfind()
    print('-----------------------------------------------------------------------------------------------------\n')
    print('In the following list we find the node\'s namespace of the generators defined in the script of interest:')
    for i in range(len(script.generators)):
        print('\n', i, ': \n', script.generators[i])
    print("----------")
    script.generatorfind()
    print('In the following list we find the namespace of the generators defined in the script of interest:')
    for i in range(len(script.generators)):
        print('\n', i, ': \n', script.generators[i])
    print("----------")
    script.assign_call_find()
    #script.findcall()
    print('LOS ASSIGNS SON LOS SIGUIENTES: ', script.assigns)
    print('LOS CALLS QUE HEMOS ENCONTRADO SON LOS SIGUIENTES: \n', script.calls)
    end = time.time()
    print("---------")
    print('Execution time:', end-start, 'seconds.')
    print('-----------------------------------------------------------------------------------------------------\n')
    


    
    
    

if __name__ == '__main__':
    main(sys.argv[1])







