import ast
import sys
import json
from ast2json import ast2json

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
            if  generators[i][-j-1].__class__.__name__.endswith('Def'):
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
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    for node in ast.walk(tree):
        #if node.__class__.__name__ == 'Call' or node.__class__.__name__ == 'Name':
        if node.__class__.__name__ == 'Name':
            for ls in generators:
                if get_name(node) == ls[0]:
                    print('1: ', ls)
                    findcall2(ls, node.lineno)

def findcall2(ls, lineno, i = 0):
    print('2: ', ls)
    for node in ast.walk(tree):
        if node.__class__.__name__ == 'Name' and node.lineno == lineno and get_name(node) == ls[i]:
            if i == len(ls) - 1:
                print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
            elif i+1 < len(ls):
                findcall2(ls, node.lineno, i+1)



'''
def findcall2(ls, lineno, i = 0):
    for node in ast.walk(tree):
        if i+1 < len(ls):
            if (node.__class__.__name__ == 'Call' or node.__class__.__name__ == 'Name') and get_name(node) == ls[i+1] and node.lineno == lineno:
                if i+1 == len(ls) -1:
                    print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                else:
                    findcall2(ls, node.lineno, i+1)

'''
def cosa():
    for node in ast.walk(tree):
        if node.__class__.__name__ == 'Call' or node.__class__.__name__ == 'Name':
            print(get_name(node))

def child_call():
    print('LOS DESCENDIENTES SON: ')
    for node in ast.walk(tree):
        if node.__class__.__name__ == 'Call' and get_name(node) == 'Clasetotal':
            print(node.lineno)
            print('Su nombre es: ', get_name(node))
            for child in ast.walk(node):
                print(child)
    print('LOS HIJOS SON: ')
    for node in ast.walk(tree):
        if node.__class__.__name__ == 'Call' and get_name(node) == 'Clasetotal':
            print(node.lineno)
            print('Su nombre es: ', get_name(node))
            for child in ast.iter_child_nodes(node):
                print(child)


def assignsearch():
    for s in range(len(generators)):
        for i in range(len(generators[s])):
            assignfind(tree, generators[s][i], generators[s], i, s)

def assignfind(node, item, sublista, i, s):
    try:
        if node.__class__.__name__ == 'Assign' and node.value.func.id==item:
            x = generators[s][:]
            x.insert(i, node.targets[0].id)
            x.pop(i+1)
            if not x in generators:
                generators.append(x)
        else:
            if ast.iter_child_nodes(node):
                for child in ast.iter_child_nodes(node):
                    assignfind(child, item, sublista, i, s)
    except AttributeError:
            pass

def findname():
    for node in ast.walk(tree):
        if node.__class__.__name__ == 'Name':
            for sublist in generators:
                if node.id == sublist[0]:
                    print('hay un Name con el nombre ', node.id, ' en la linea ', node.lineno)


def saveast():
    astprint = ast2json(tree)
    f = open("astree.txt", "w")
    f.write(json.dumps(astprint, indent=4))
    f.close()

def main():
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


if __name__ == '__main__':
    tree = sys.argv[1]
    generators = []
    main()


