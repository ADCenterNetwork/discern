import ast
import sys, os
import json
from ast2json import ast2json
import time

def get_name(node):
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
    tree = ast.parse(open(sys.argv[1]).read())
    astprint = ast2json(tree)
    f = open("astree.txt", "w")
    f.write(json.dumps(astprint, indent=4))
    f.close()

def _get_folder(filename):
    path = os.path.split(filename)[0]
    full_path = os.path.join(os.getcwd(), path)
    return full_path

class Code():
    def __init__(self, name):
        self.tree = ast.parse(open(name).read())
        self.generators = []
        self.path = name
        self.calls = {}
        self.assigns = {}
    
    def yieldfind(self, node = None, ls = []):
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
        if node == None:
            node = self.tree
        if isinstance(node, ast.Assign):
            name = node.targets[0].id
            if name not in self.assigns.keys():
                self.assigns[name] = []
            for child in ast.iter_child_nodes(node):
                self.assignsearch(name, child)
        if ast.iter_child_nodes(node):
            for child in ast.iter_child_nodes(node):
                self.assign_call_find(child)
        
    def assignsearch(self,new_name, node):
        #node is a descendent from an assign, though not necessarily a call
        if isinstance(node, ast.Call):
            func_name = get_name(node)
            self.assigns[new_name].insert(0, func_name)
        if ast.iter_child_nodes(node):
            for child in ast.iter_child_nodes(node):
                self.assignsearch(new_name, child)

    '''
    def assignsearch(self):
        for s in range(len(self.generators)):
                self.__assignfind(self.tree, self.generators[s][:], self.generators[s], 0, s, [], []) 
        '''
        
    def __assignfind(self, node, item, sublista, i, s, *args, **kwargs):

        if isinstance(node,  ast.ClassDef ) or isinstance(node,  ast.FunctionDef ) :
            return
            # Skip Classes and Functions 

        elif isinstance(node,  ast.Expr):
            #TO DO or TO Delete
            pass

        elif isinstance(node,  ast.Assign):
            #TO DO
            #print(node.__class__.__name__, node.targets[0].id, node.targets[0].lineno)
            for __tree in ast.walk(node):
                if isinstance(__tree,  ast.Call):
                    print(__tree.__class__.__name__, get_name(__tree))
                    if get_name(__tree) in self.generators[s][:]:
                        self.assigns[get_name(__tree)] = node.targets[0].id
                        #print(self.assigns)             
            pass
        # TO Change  
        elif  isinstance(node,  ast.Call) and not isinstance(ast.iter_child_nodes(node), ast.Call) :
            if isinstance(node,  ast.Name):
               pass

        elif  isinstance(node,  ast.Attribute):
            pass

        elif  isinstance(node,  ast.Name):
            pass
        
        elif isinstance(node, ast.Store) or isinstance(node, ast.Load):
            pass   

        #End TO Change
        else:
            if ast.iter_child_nodes(node):
                for child in ast.iter_child_nodes(node):
                    self.__assignfind(child, item, sublista, i+1, s, args)


    def findcall(self):
        for node in ast.walk(self.tree):
            if node.__class__.__name__ == 'Call':
                for ls in self.generators:
                    if get_name(node) == ls[0]:
                        if len(ls) > 1:
                            self.findcall2(ls, node.lineno)
                        else:
                            try:
                                self.calls[tuple(ls)].append(node.lineno)
                            except KeyError:
                                self.calls[tuple(ls)] = [node.lineno]
                            print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
            elif node.__class__.__name__ == 'Name':
                for ls in self.generators:
                    if node.id == ls[0]:
                        if len(ls) > 1:
                            self.findcall2(ls, node.lineno)
                        else:
                            try:
                                self.calls[tuple(ls)].append(node.lineno)
                            except KeyError:
                                self.calls[tuple(ls)] = [node.lineno]
                            print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
            
            elif node.__class__.__name__ == 'Attribute':
                for ls in self.generators:
                    if node.value == ls[0]:
                        if len(ls) > 1:
                            self.findcall2(ls, node.lineno)
                        else:
                            try:
                                self.calls[tuple(ls)].append(node.lineno)
                            except KeyError:
                                self.calls[tuple(ls)] = [node.lineno]
                            print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)

    def findcall2(self, ls, lineno, i = 0):
        #try:
            for node in ast.walk(self.tree):
                if node.__class__.__name__ == 'Call' and get_name(node) == ls[i+1] and node.lineno == lineno:
                    if i+1 == len(ls) -1:
                        try:
                                self.calls[tuple(ls)].append(node.lineno)
                        except KeyError:
                                self.calls[tuple(ls)] = [node.lineno]
                        print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                    else:
                        self.findcall2(ls, node.lineno, i+1)
                elif node.__class__.__name__ == 'Name' and node.id == ls[i+1] and node.lineno == lineno:
                    if i+1 == len(ls) -1:
                        try:
                                self.calls[tuple(ls)].append(node.lineno)
                        except KeyError:
                                self.calls[tuple(ls)] = [node.lineno]
                        print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                    else:
                        self.findcall2(ls, node.lineno, i+1)
                elif node.__class__.__name__ == 'Attribute' and node.value == ls[i+1] and node.lineno == lineno:
                        if i+1 == len(ls) -1:
                            try:
                                self.calls[tuple(ls)].append(node.lineno)
                            except KeyError:
                                self.calls[tuple(ls)] = [node.lineno]
                            print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                        else:
                            self.findcall2(ls, node.lineno, i+1)
        #except IndexError:
            #pass




def main(name):
    start = time.time()
    script = Code(name)
    saveast()      
    script.yieldfind()
    for i in range(len(script.generators)):
        print('\n', i, ': \n', script.generators[i])
    script.generatorfind()
    for i in range(len(script.generators)):
        print('\n', i, ': \n', script.generators[i])
    print("----------")
    #script.assignsearch()
    script.assign_call_find()
    for i in range(len(script.generators)):
        print('\n', i, ': \n', script.generators[i])
    script.findcall()
    print('LOS ASSIGNS SON LOS SIGUIENTES: ', script.assigns)
    print('LOS CALLS QUE HEMOS ENCONTRADO SON LOS SIGUIENTES: \n', script.calls)
    end = time.time()
    print("---------")
    print(end-start)
    


    
    
    

if __name__ == '__main__':
    main(sys.argv[1])







