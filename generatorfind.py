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
'''
def _get_folder(filename):
    for i in range(len(filename)-1):
        j = -i-1
        if filename[j] == '\\':
            path = filename[0:j]
            break
    full_path = os.path.join(os.getcwd(), path)
    return full_path
'''
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
    
    def yieldfind(self, node = None, ls = []):
        if node == None:
            node = self.tree
        if node.__class__.__name__ == 'Import':
            for i in range(len(node.names)):
                ls.append(node)
                folder = _get_folder(self.path)
                imported_file = os.path.join(folder, node.names[i].name+'.py')
                #tree2 = ast.parse(open(node.names[i].name+'.py').read())
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
        for i in range(len(self.generators)):
            for j in range(len(self.generators[i])-1): 
                if  self.generators[i][-j-1].__class__.__name__ == "FunctionDef" :
                    self.generators[i] = self.generators[i][1:-j]
                    break
            for j in range(len(self.generators[i])):
                if not self.generators[i][j].__class__.__name__ =='Import' and not self.generators[i][j].__class__.__name__ =='Module':
                    self.generators[i][j] = self.generators[i][j].name
                elif self.generators[i][j].__class__.__name__ =='Import':
                    if self.generators[i][j].names[0].asname:
                        self.generators[i][j] = self.generators[i][j].names[0].asname
                    else:
                        self.generators[i][j] = self.generators[i][j].names[0].name
                else:
                    self.generators[i][j]=None
            self.generators[i] = [x for x in self.generators[i] if x is not None]
    def assign_call_find(self, node = None):
        if node == None:
            node = self.tree
        for child in ast.iter_child_nodes(node):
            pass
            #__asignfind()
            #findcall()

    def assignsearch(self):
        for s in range(len(self.generators)):
                self.__assignfind(self.tree, self.generators[s][:], self.generators[s], 0, s, [], [])             
    '''
        for s in range(len(self.generators)):
            #for i in range(len(self.generators[s])):
                self.__assignfind(self.tree, self.generators[s][:], self.generators[s], 0, s, [], [])
    '''          
    def __assignfind(self, node, item, sublista, i, s, *args, **kwargs):

        if isinstance(node,  ast.ClassDef ) or isinstance(node,  ast.FunctionDef ) :
            return
            # Skip Classes and Functions

        elif isinstance(node,  ast.Expr):
            #TO DO
            pass

        elif isinstance(node,  ast.Assign):
            #TO DO
            for __tree in ast.walk(node):
                if isinstance(__tree,  ast.Call):
                    #TO DO: 
                    #print(__tree.__class__.__name__, get_name(__tree))
                    #x = [node.targets[0].id,get_name(__tree)] 
                    x = self.generators[s][:]
                    x.insert(i-1, node.targets[0].id)
                    x.pop(i)
                    if not x in self.generators:
                        self.generators.append(x) 
                        #x = self.generators[s][:]
                        #x.insert(0, node.value.id)              
            pass
        # TO Change  
        elif  isinstance(node,  ast.Call) and not isinstance(ast.iter_child_nodes(node), ast.Call) :
            print(node.__class__.__name__, get_name(node))
            
            if isinstance(node,  ast.Name):
                print("     "+node.__class__.__name__, get_name(node))
            pass

        elif  isinstance(node,  ast.Attribute):
            print(node.__class__.__name__, get_name(node))
            pass

        elif  isinstance(node,  ast.Name):
            print(node.__class__.__name__, get_name(node))
      
        
        elif isinstance(node, ast.Store) or isinstance(node, ast.Load):
            print("no more child")
            pass   
        #End TO Change
        else:
            if ast.iter_child_nodes(node):
                for child in ast.iter_child_nodes(node):
                    self.__assignfind(child, item, sublista, i+1, s, args)

        '''
        if  isinstance(node,  ast.Assign) :
            #isinstance(node,  ast.Attribute)  or isinstance(node,  ast.Assign) or  :
            # #node.__class__.__name__ == 'Assign' : #(node.__class__.__name__ == 'Attribute' or node.__class__.__name__ == 'Name'):# and (node.value.func.id==item or "generator"==item):
                #for child in ast.iter_child_nodes(node):    
                #if isinstance(item, node.attr) or isinstance(item, node.id) :
                #if get_name(item):
                #if item == node.attr :
                #if item == node.value.id or item ==node :
                    list(args).insert(i, node.targets[0].id) 
                    #x.insert(i, node.id)
                    #x.pop(i+1)

                    
                    if not x in generators:
                        generators.append(x)
                    

        elif isinstance(node,  ast.Expr):
            pass
        #elif isinstance(node,  ast.Call) :#and not isinstance(ast.iter_child_nodes(node), ast.Call):
        elif  isinstance(node,  ast.Attribute) :
            print(node.__class__.__name__)
            #print(args)
            #if item == node.attr :
            x = self.generators[s][:]
            x.insert(0, node.value.id) 
            #x.insert(0, node.func.value.id)
            if not x in self.generators:
                self.generators.append(x)
        else:
            if isinstance(node,  ast.ClassDef ) or isinstance(node,  ast.FunctionDef ) :
                return
            if ast.iter_child_nodes(node):
                for child in ast.iter_child_nodes(node):
                    self.__assignfind(child, item, sublista, i, s, args)
        '''

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
    script.assignsearch()
    for i in range(len(script.generators)):
        print('\n', i, ': \n', script.generators[i])
    script.findcall()
    print('LOS CALLS QUE HEMOS ENCONTRADO SON LOS SIGUIENTES: \n', script.calls)
    end = time.time()
    print("---------")
    print(end-start)
    


    
    
    

if __name__ == '__main__':
    main(sys.argv[1])







