from ..generatorfind.generatorfind import Code
import ast
import os, pytest, shutil

# READ BEFORE RUNNING TEST:
# Sometimes, when running all test simultaneously, some test appears in red (apparently failed), If this happens,
#just run every failed test individually and they will work succesfully.

path = os.path.join(os.getcwd(), 'tests', 'pruebas.py')
prueba = Code(path)
path2 = os.path.join(os.getcwd(), 'tests', 'pruebas2.py')
pruebas2 = Code(path2)

#@pytest.fixture
def yieldnodes():
    """yieldnodes works in pruebas.py: we detect its generators and we save the namespace's nodes of this 
    generators.

    Returns:
        [list]: [list containing the node type of namespace's nodes.]
    """
    prueba.yieldfind()
    res = []
    for sublist in prueba.generators:
        res.append([])
        for node in sublist:
            res[-1].append(node.__class__.__name__)
    return res

#@pytest.fixture
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

#@pytest.fixture
def namespaces():
    """namespaces works in pruebas.py and it get the namespace of the generators in pruebas.py.

    Returns:
        [list]: [list containing the namespaces of the generators.]
    """
    prueba.yieldfind()
    prueba.generatorfind()
    return prueba.generators

#@pytest.fixture
def namespaces2():
    """namespaces2 works in pruebas2.py and it get the namespace of the generators in pruebas2.py.

    Returns:
        [list]: [list containing the namespaces of the generators.]
    """
    pruebas2.yieldfind()
    pruebas2.generatorfind()
    return pruebas2.generators

def test_yieldfind():
    """test_yieldfind asserts yieldnodes obtains the expected value. 
    """
    nodeclasses = yieldnodes()   #print(nodeclasses)
    assert nodeclasses == [['Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'], \
        ['Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'],\
        ['Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'], \
        ['Module','FunctionDef', 'FunctionDef', 'FunctionDef', 'While', 'Expr', 'Yield'], ['Module','FunctionDef','Expr', 'Yield']]
        

def test_generatorfind():
    """test_generatorfind asserts that namespaces obtains the expected value.
    """
    namespace = namespaces()
    assert namespace == [['Clase1_1', 'Clase1_2', 'firstn'], \
        ['Clase1_1', 'Clase1_3', 'firstn'], \
        ['Clase2_1', 'Clase2_2', 'firstn'], ['primera', 'segunda', 'qsfn'], ['generator']]


def test_yieldfind2():
    """test_yieldfind2 asserts yieldnodes2 obtains the expected value. 
    """
    nodeclasses = yieldnodes2()
    assert nodeclasses == [['Module', 'Import', 'Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'], \
        ['Module', 'Import', 'Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'],\
        ['Module', 'Import', 'Module', 'ClassDef', 'ClassDef', 'FunctionDef','While','Expr', 'Yield'], \
        ['Module', 'Import', 'Module', 'FunctionDef', 'FunctionDef', 'FunctionDef', 'While', 'Expr', 'Yield'], \
        ['Module', 'Import', 'Module', 'FunctionDef','Expr', 'Yield'], \
        ['Module', 'Import', 'Module', 'Module', 'ClassDef', 'ClassDef', 'FunctionDef','Expr', 'Yield'], \
        ['Module', 'Import', 'Module', 'Module', 'FunctionDef','Expr', 'Yield']]
        

def test_generatorfind2():
    """test_generatorfind2 asserts that namespaces2 obtains the expected value.
    """
    namespace = namespaces2()
    assert namespace == [['pruebas', 'Clase1_1', 'Clase1_2', 'firstn'], \
        ['pruebas', 'Clase1_1', 'Clase1_3', 'firstn'], \
        ['pruebas', 'Clase2_1', 'Clase2_2', 'firstn'], \
        ['pruebas', 'primera', 'segunda', 'qsfn'], \
        ['pruebas', 'generator'], \
        ['prueba_simple', 'Clase1', 'Clase2', 'f'], \
        ['prueba_simple', 'f']]

