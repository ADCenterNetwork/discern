import ast
import sys

def get_parent(tree):
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node


def generatorfind(tree, filename):
    functions = []
    for node in ast.walk(tree):
        if node.__class__.__name__ == 'Yield':
            parent = node.parent
            while not parent.__class__.__name__ == 'FunctionDef':
                parent = parent.parent
            num = parent.lineno
            content = open(filename).readlines()
            funcion = content[num - 1]
            while funcion.startswith(' '):
                funcion = funcion.strip(' ')
            funcion = funcion.strip('def')
            while funcion.startswith(' '):
                funcion = funcion.strip(' ')
            funcion = funcion.split('(')
            funcion = funcion[0]
            functions.append(funcion)
            functions = list(dict.fromkeys(functions))
    return functions

def findgenerator(filename):
    tree = ast.parse(open(filename).read())
    get_parent(tree)
    functions = []
    for node in ast.walk(tree):
        if node.__class__.__name__ == 'Yield':
            parent = node.parent
            while not parent.__class__.__name__ == 'FunctionDef':
                parent = parent.parent
            num = parent.lineno
            content = open(filename).readlines()
            funcion = content[num - 1]
            while funcion.startswith(' '):
                funcion = funcion.strip(' ')
            funcion = funcion.strip('def')
            while funcion.startswith(' '):
                funcion = funcion.strip(' ')
            funcion = funcion.split('(')
            funcion = funcion[0]
            functions.append(funcion)
            functions = list(dict.fromkeys(functions))
    return functions


    

def main():
    script = sys.argv[1]
    tree = ast.parse(open(script).read())
    get_parent(tree)
    print(generatorfind(tree, script))



if __name__ == '__main__':
    main()