import ast
import sys
import json
from ast2json import ast2json
import time

def yieldfind(node, ls):
    if node.__class__.__name__ == 'Yield':
        ls.append(node)
        x = ls[:]
        generators.append(x)
    else:
        if ast.iter_child_nodes(node):
            ls.append(node)
            for child in ast.iter_child_nodes(node):
                y = ls[:]
                yieldfind(child, y)
                

    
def generatorfind():
    for i in range(len(generators)):
        for j in range(len(generators[i])-1): 
            print(generators[i][-j-1].__class__.__name__) 
            if  generators[i][-j-1].__class__.__name__ == "FunctionDef" :
                generators[i] = generators[i][1:-j]
                break
        for j in range(len(generators[i])):
            generators[i][j] = generators[i][j].name 
            

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

def findcall():
    for node in ast.walk(tree):
        if node.__class__.__name__ == 'Call':
            for ls in generators:
                if get_name(node) == ls[0]:
                    findcall2(ls, node.lineno)
        elif node.__class__.__name__ == 'Name':
            for ls in generators:
                if node.id == ls[0]:
                    findcall2(ls, node.lineno)
        
        elif node.__class__.__name__ == 'Attribute':
            for ls in generators:
                if node.value == ls[0]:
                    findcall2(ls, node.lineno)
        

def findcall2(ls, lineno, i = 0):
        try:
            for node in ast.walk(tree):
                if node.__class__.__name__ == 'Call' and get_name(node) == ls[i+1] and node.lineno == lineno:
                    if i+1 == len(ls) -1:
                        print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                    else:
                        findcall2(ls, node.lineno, i+1)
                elif node.__class__.__name__ == 'Name' and node.id == ls[i+1] and node.lineno == lineno:
                    if i+1 == len(ls) -1:
                        print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                    else:
                        findcall2(ls, node.lineno, i+1)
                else:
                    if node.__class__.__name__ == 'Attribute' and node.value == ls[i+1] and node.lineno == lineno:
                        if i+1 == len(ls) -1:
                            print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                        else:
                            findcall2(ls, node.lineno, i+1)
        except IndexError:
            pass
        

def assignsearch():
    print(generators)
    for s in range(len(generators)):
        #for i in range(len(generators[s])):
            assignfind(tree, generators[s][-1], generators[s], s)


def assignfind(node, item, sublista,  s):
    try:
        if (node.__class__.__name__ == 'Attribute'):# and (node.value.func.id==item or "generator"==item):
            if item == node.attr :
                x = generators[s][:]
                x.insert(0, node.value.id) 
                if not x in generators:
                    generators.append(x)
        else:
            if ast.iter_child_nodes(node):
                for child in ast.iter_child_nodes(node):
                    
                    assignfind(child, item, sublista, s)
    except AttributeError:
            pass


def saveast():
    astprint = ast2json(tree)
    f = open("astree.txt", "w")
    f.write(json.dumps(astprint, indent=4))
    f.close()

def main():
    start = time.time()
    script = sys.argv[1]
    global tree
    tree = ast.parse(open(script).read())
    global generators
    generators = []
    saveast()      
    yieldfind(tree, [])
    for i in range(len(generators)):
        print('\n', i, ': \n', generators[i])
    generatorfind()
    for i in range(len(generators)):
        print('\n', i, ': \n', generators[i])
    print("----------")
    assignsearch()
    for i in range(len(generators)):
        print('\n', i, ': \n', generators[i])
    findcall()
    end = time.time()
    print("---------")
    print(end-start)
    #child_call()
    


    
    
    

if __name__ == '__main__':
    main()

