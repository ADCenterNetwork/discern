import ast
import sys
import json
from ast2json import ast2json

"""Generator Find (provisional name).
   
   This program is still under construction.

    For now, this program is able to detect all the generators existing in an external file with a 
   correct namespace and check all the calls to that generators. As a bonus, it saves on an external 
   .txt file the tree of the interested python file.

   This program can be executed directly from the command prompt with: python generatorfindv2.py file.py
   where file.py is the file in wich we are interested.
   """

# In order to detect generators, we search 'Yield's nodes and we walk up the tree branch, saving 
#the nodes that contain that yield node solving namespacing problems.  
def yieldfind(node, ls):
    if node.__class__.__name__ == 'Import':
        for i in range(len(node.names)):
            ls.append(node)
            tree2 = ast.parse(open(node.names[i].name+'.py').read())
            yieldfind(tree2, ls)
    elif node.__class__.__name__ == 'Yield':
        ls.append(node)
        x = ls[:]
        generators.append(x)
    else:
        if ast.iter_child_nodes(node):
            ls.append(node)
            for child in ast.iter_child_nodes(node):
                y = ls[:]
                yieldfind(child, y)

# With yieldfind we obtain in a list all the nodes that contain the generator. With generatorfind
#we filter the name of functions or classes "callables" saving the namespace.
def generatorfind():
    for i in range(len(generators)):
        for j in range(len(generators[i])-1):
            if  generators[i][-j-1].__class__.__name__.endswith('Def'):# or generators[i][-j-1].__class__.__name__=='Import':
                generators[i] = generators[i][1:-j]
                break
        for j in range(len(generators[i])):
            if not generators[i][j].__class__.__name__ =='Import' and not generators[i][j].__class__.__name__ =='Module':
                generators[i][j] = generators[i][j].name
            elif generators[i][j].__class__.__name__ =='Import':
                if generators[i][j].names[0].asname:
                    generators[i][j] = generators[i][j].names[0].asname
                else:
                    generators[i][j] = generators[i][j].names[0].name
            else:
                    generators[i][j]=None#.remove(generators[i][j])
        generators[i] = [x for x in generators[i] if x is not None]

# We will check periodically the name of the diferent nodes in order to detect calls. It is usefull to
#have a function that makes it automatically.
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
                    x = node.names[0].name
                    return x
                except AttributeError:
                    try:
                        x = node.value.args[0].id
                        return x
                    except AttributeError:
                        return None

# We introduce a list with all the namespace of the generators into findcall and findcall2. This two functions
#work together and they are the heart of this program. The idea is to walk up the tree checking diferent calls
#to the generators on our list and will return all the calls in the script of interest. 
#This two functions detect the calls depending of the differents way of calling the generator, and it still 
#does not contemplate all the cases.  
def findcall():
    called=[]
    for node in ast.walk(tree):
        if node.__class__.__name__ == 'Call' or node.__class__.__name__ == 'Name' or node.__class__.__name__ =='Expr':
            for ls in generators:
                if get_name(node) == ls[0]:
                    findcall2(ls, node.lineno, called)
def findcall2(ls, lineno, called, i = 0):
    for node in ast.walk(tree):
        if i+1 <= len(ls):
            try:
                if (node.__class__.__name__ == 'Call' or node.__class__.__name__ == 'Name' or node.__class__.__name__ == 'Expr') and get_name(node) == ls[i+1] and node.lineno == lineno:
                    if i+1 == len(ls) -1:
                        print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                    else:
                        findcall2(ls, node.lineno, i+1)
            except IndexError:    
                if get_name(node) == ls[i] and node.lineno == lineno:
                    if [ls, node.lineno] not in called:
                        print('Hemos encontrado el call de ', ls, ' en la linea ', node.lineno)
                        called.append(ls.append(lineno))

# This is a function that has the objective to help us when we want to study the different ast.
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

# With assignsearch and assignfind we will be able to detect and include the rename of the different
#generators on our list, because the new generators created by rename old generators are also interesting. 
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

# Saveast is a function created in order to help us to visualize the ast on an external .txt file.
def saveast():
    astprint = ast2json(tree)
    f = open("astree.txt", "w")
    f.write(json.dumps(astprint, indent=4))
    f.close()

class Code:
    def __init__(self, name):
        self.name = name
    def tree(self):
        x = ast.parse(open(self.name).read())
        return x

def main():
    script = sys.argv[1]
    print(Code().tree())
    global generators
    generators = []
    saveast()      
    yieldfind(tree, [])
    generatorfind()
    print("----------")
    assignsearch()
    for i in range(len(generators)):
        print('\n', i, ': \n', generators[i])
    print("\n---------")
    findcall()
    print("\n---------")
    #child_call()


    
    
    

if __name__ == '__main__':
    main()

