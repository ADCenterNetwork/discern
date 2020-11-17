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

for node in ast.walk(tree):
    if node.__class__.__name__ == 'Call':
        try:
            dc[node.lineno] += 1
        except KeyError:
            dc[node.lineno] = 1

for keys in dc:
    print(keys, ': ', dc[keys], '\n')


print('#####################################')


dc = {}

for node in ast.walk(tree):
    if node.__class__.__name__ == 'Name':
        print(node, get_name(node), node.lineno)
        try:
            dc[node.lineno] += 1
        except KeyError:
            dc[node.lineno] = 1

for keys in dc:
    print(keys, ': ', dc[keys], '\n')

