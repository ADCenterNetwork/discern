import ast
import sys
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
                return None


def saveast():
    tree = ast.parse(open(sys.argv[1]).read())
    astprint = ast2json(tree)
    f = open("astree.txt", "w")
    f.write(json.dumps(astprint, indent=4))
    f.close()

class Code():
    def __init__(self, name):
        self.tree = ast.parse(open(name).read())
        self.generators = []
    
    def yieldfind(self, node = None, ls = []):
        if node == None:
            node = self.tree
        if node.__class__.__name__ == 'Import':
            for i in range(len(node.names)):
                ls.append(node)
                tree2 = ast.parse(open(node.names[i].name+'.py').read())
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

    def assignsearch(self):
        print(self.generators)
        for s in range(len(self.generators)):
                self.__assignfind(self.tree, self.generators[s][-1], self.generators[s], s)

    def __assignfind(self, node, item, sublista,  s):
        try:
            if (node.__class__.__name__ == 'Attribute'):# and (node.value.func.id==item or "generator"==item):
                if item == node.attr :
                    x = self.generators[s][:]
                    x.insert(0, node.value.id) 
                    if not x in self.generators:
                        self.generators.append(x)
            else:
                if ast.iter_child_nodes(node):
                    for child in ast.iter_child_nodes(node):
                        self.__assignfind(child, item, sublista, s)
        except AttributeError:
                pass

    """ We still have to modify succesfully __assignfind to be able to detect multiples assignments.
        def __assignfind(self, node, item, sublista, s):
            if node.__class__.__name__=='Import':
                for n in range(len(node.names)):
                    if node.names[n].asname==self.generators[s][0]:
                        tree2 = ast.parse(open(node.names[n].name+'.py').read())
                        self.__assignfind(tree2, item, sublista, s)
            else:
                try:
                    if (node.__class__.__name__ == 'Attribute') and item == node.attr:# and (node.value.func.id==item or "generator"==item):
                        x = self.generators[s][:]
                        x.insert(self.generators[s].index(item)-1, node.value.id) 
                        x.pop(self.generators[s].index(item))
                        if not x in self.generators:
                            self.generators.append(x)
                        print(self.generators[s].index(item), len(self.generators[s])-1)
                    elif node.__class__.__name__ == 'Name' and item==get_name(node):
                        print(node.__dict__, node.__class__.__name__)
                        x = self.generators[s][:]
                        x.insert(self.generators[s].index(item)-1, node.value.id) 
                        x.pop(self.generators[s].index(item))
                        if not x in self.generators:
                            self.generators.append(x)
                    else:
                        if ast.iter_child_nodes(node):
                            for child in ast.iter_child_nodes(node):
                                self.__assignfind(child, item, sublista, s)
                except AttributeError:
                        pass
    """

    def findcall(self):
        for node in ast.walk(self.tree):
            if node.__class__.__name__ == 'Call':
                for ls in self.generators:
                    if get_name(node) == ls[0]:
                        if len(ls) > 1:
                            self.findcall2(ls, node.lineno)
                        else:
                            print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
            elif node.__class__.__name__ == 'Name':
                for ls in self.generators:
                    if node.id == ls[0]:
                        if len(ls) > 1:
                            self.findcall2(ls, node.lineno)
                        else:
                            print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
            
            elif node.__class__.__name__ == 'Attribute':
                for ls in self.generators:
                    if node.value == ls[0]:
                        if len(ls) > 1:
                            self.findcall2(ls, node.lineno)
                        else:
                            print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)

    def findcall2(self, ls, lineno, i = 0):
        #try:
            for node in ast.walk(self.tree):
                if node.__class__.__name__ == 'Call' and get_name(node) == ls[i+1] and node.lineno == lineno:
                    if i+1 == len(ls) -1:
                        print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                    else:
                        self.findcall2(ls, node.lineno, i+1)
                elif node.__class__.__name__ == 'Name' and node.id == ls[i+1] and node.lineno == lineno:
                    if i+1 == len(ls) -1:
                        print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                    else:
                        self.findcall2(ls, node.lineno, i+1)
                elif node.__class__.__name__ == 'Attribute' and node.value == ls[i+1] and node.lineno == lineno:
                        if i+1 == len(ls) -1:
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
    end = time.time()
    print("---------")
    print(end-start)
    


    
    
    

if __name__ == '__main__':
    main(sys.argv[1])







