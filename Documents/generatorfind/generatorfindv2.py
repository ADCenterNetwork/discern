import ast
import sys

def get_parent(tree):
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node


def generatorfind(tree, filename):
    functions = []
    for node in ast.walk(tree):
        if str(node).startswith('<_ast.Yield'):
            parent = node.parent
            while not str(parent).startswith('<_ast.FunctionDef'):
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
        if str(node).startswith('<_ast.Yield'):
            parent = node.parent
            while not str(parent).startswith('<_ast.FunctionDef'):
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

class FindCall(ast.NodeVisitor):
    def __init__(self, *args):
        if len(args) < 1:
            raise ValueError("Must supply at least ine target function")
        self.result = {arg: [] for arg in args}    
    def visit_Call(self, node):
        if node.func.id in self.result:
            #self.result[node.func.id].append(map(ast.literal_eval, node.args))
            self.result[node.func.id].append(dict(object = node, linea= node.lineno ))
        # visit the children
        self.generic_visit(node)
    

def main():
    script = sys.argv[1]
    tree = ast.parse(open(script).read())
    get_parent(tree)
    print(generatorfind(tree, script))

    lista= generatorfind(tree, script)

    for i in lista:
        fc = FindCall(i)
        fc.visit(tree)
        print(fc.result)

if __name__ == '__main__':
    main()