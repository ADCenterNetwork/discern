import ast
import sys



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

with open(sys.argv[1]) as f:
    content = f.read()

tree = ast.parse(content)

dc = {}
dc2 = {}
dc3 = {}

def funcion(node):
    for child in ast.iter_child_nodes(node):
        if child.__class__.__name__ == 'Call':
            print(get_name(child))
        funcion(child)

for node in ast.walk(tree):
    if node.__class__.__name__ == 'Call':
        if get_name(node) == 'firstn':
            if node.lineno == 68:
                funcion(node)




'''

for node in ast.walk(tree):
    if node.__class__.__name__ == 'Call':
        try:
            dc[node.lineno] += 1
        except KeyError:
            dc[node.lineno] = 1
    elif node.__class__.__name__ == 'Name':
        try:
            dc2[node.lineno] += 1
        except KeyError:
            dc2[node.lineno] = 1
    elif node.__class__.__name__ == 'Attribute':
        try:
            dc3[node.lineno] += 1
        except KeyError:
            dc3[node.lineno] = 1

print('Los de tipo CALL son: \n')
for keys in dc:
    print(keys, ': ', dc[keys])

print('Los de tipo NAME son: \n')
for keys in dc2:
    print(keys, ': ', dc2[keys])

print('Los de tipo ASSIGN son: \n')
for keys in dc3:
    print(keys, ': ', dc3[keys])



def tree_walker(node):
    for child in ast.iter_child_nodes(node):
        if child.__class__.__name__ == 'Call':
            ls = [granchild for granchild in ast.iter_child_nodes(child)]
            print('Tenemos un nodo Call en la linea ', child.lineno, ' y de nombre ', get_name(child) )
            print('Sus hijos son: ', ls)
        tree_walker(child)

tree_walker(tree)


def tree_walker_names(node):
    for child in ast.iter_child_nodes(node):
        if child.__class__.__name__ == 'Name':
            ls = [granchild for granchild in ast.iter_child_nodes(child)]
            print('Tenemos un nodo Name en la linea ', child.lineno, ' y de nombre ', get_name(child) )
            print('Sus hijos son: ', ls)
        tree_walker_names(child)

tree_walker_names(tree)
'''