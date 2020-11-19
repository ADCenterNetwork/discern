from ..generatorfind.generatorfind import Code
import ast
import os, pytest, shutil




path = os.path.join(os.getcwd(), 'tests', 'pruebas.py')
prueba = Code(path)

path2 = os.path.join(os.getcwd(), 'tests', 'pruebas2.py')
pruebas2 = Code(path2)



yieldfind = prueba.yieldfind
generatorfind = prueba.generatorfind
assignsearch = prueba.assignsearch
findcall = prueba.findcall

#@pytest.fixture
def yieldnodes():
    """yieldnodes works in pruebas.py: we detect its generators and we save the namespace's nodes of this 
    generators.
 
    Returns:
        [list]: [list containing the node type of namespace's nodes.]
    """
    yieldfind()
    res = []
    for sublist in prueba.generators:
        res.append([])
        for node in sublist:
            res[-1].append(node.__class__.__name__)
    return res


def yieldnodes2():
    """yieldnodes2 works in pruebas2.py: we detect its generators and we save the namespace's nodes of this 
    generators.
 
    Returns:
        [list]: [list containing the node type of namespace's nodes.]
    """
    pruebas2.yieldfind()
    res = []
    for sublist in pruebas2.generators:
        res.append([])
        for node in sublist:
            res[-1].append(node.__class__.__name__)
    return res

def test_yieldfind():
    res = yieldnodes()
    assert res == [['Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'], \
        ['Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'],\
        ['Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'], \
        ['Module','FunctionDef', 'FunctionDef', 'FunctionDef', 'While', 'Expr', 'Yield'], ['Module','FunctionDef','Expr', 'Yield']]

'''
def test_yieldfind2():
    """test_yieldfind2 asserts yieldnodes2 obtains the expected value. 
    """
    nodeclasses = yieldnodes2()
    print(nodeclasses)
    assert nodeclasses == [['Module','Module', 'Import', 'Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'], \
        ['Module','Module', 'Import', 'Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'],\
        ['Module','Module', 'Import', 'Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'], \
        ['Module','Module', 'Import', 'Module', 'FunctionDef', 'FunctionDef', 'FunctionDef', 'While', 'Expr', 'Yield'], \
        ['Module','Module', 'Import', 'Module', 'FunctionDef','Expr', 'Yield'], \
        ['Module','Module', 'Import', 'Module', 'Module', 'ClassDef', 'ClassDef', 'FunctionDef','Expr', 'Yield'], \
        ['Module','Module', 'Import', 'Module', 'Module', 'FunctionDef','Expr', 'Yield']]
        '''


def test_generatorfind():
    generatorfind()
    print(prueba.generators)
    assert prueba.generators == [['Clase1_1', 'Clase1_2', 'firstn'], \
        ['Clase1_1', 'Clase1_3', 'firstn'], \
        ['Clase2_1', 'Clase2_2', 'firstn'], ['primera', 'segunda', 'qsfn'], ['generator']]

