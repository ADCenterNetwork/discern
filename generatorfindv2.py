import ast
import sys

def get_parent(tree):
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

def generatorfind(tree):
    functions = []
    for node in ast.walk(tree):
        if node.__class__.__name__ == "Yield":
            namespace = []
            parent = node.parent
            while not parent.__class__.__name__ == "Module":
                if parent.__class__.__name__ == "FunctionDef" or parent.__class__.__name__ == "ClassDef":
                    #namespace.append(parent.name)
                    namespace.insert(0,parent.name)
                parent = parent.parent  
            functions.append(namespace)
    #zipped = list(zip(functions, nodefunc))
    return functions

def findgenerator(filename):
    global tree
    tree = ast.parse(open(filename).read())
    get_parent(tree)
    functions = generatorfind(tree)
    return functions

class FindCall(ast.NodeVisitor):
    def __init__(self, *args):
        if len(args) < 1:
            raise ValueError("Must supply at least ine target function")
        self.result = {arg: [] for arg in args}    
    def visit_Call(self, node):
        if node.func.id in self.result:
            self.result[node.func.id].append(dict(call = node, linea= node.lineno ))
        self.generic_visit(node)
    
def findcall(lista):
    for i in range(len(lista)):
        fc = FindCall(lista[i][0])
        fc.visit(tree)
        return fc.result

def main():
    script = sys.argv[1]
    global tree
    tree = ast.parse(open(script).read())
    get_parent(tree)
    print(generatorfind(tree))
    lista= generatorfind(tree)
    calls = findcall(lista)
    print(calls)

#con zip
    #for i in range(len(lista)):
    #    fc=FindCall(lista[i][0][0])
    #    fc.visit(tree)
    #    print(fc.result)
    
    

if __name__ == '__main__':
    main()