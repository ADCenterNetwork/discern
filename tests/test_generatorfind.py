from ..generatorfind.generatorfind import Discern, FolderCalls
import ast
import os, pytest, shutil


@pytest.fixture
def setup():
    path = os.path.join(os.getcwd(), 'tests', 'pruebas.py')
    prueba = Discern(path)
    return prueba

@pytest.fixture
def setup_imports():
    path_imports = os.path.join(os.getcwd(), 'tests', 'pruebas2.py')
    prueba_imports = Discern(path_imports)
    return prueba_imports


@pytest.fixture
def setup_multiple_assign():
    path = os.path.join(os.getcwd(), 'tests', 'multiple_assign.py')
    prueba = Discern(path)
    return prueba

@pytest.fixture
def setup_folder():
    path = os.path.join(os.getcwd(), 'tests', 'folder')
    prueba = FolderCalls(path)
    return prueba

def test_namespace_pruebas(setup):
    """test_namespace_pruebas asserts that namespaces obtains the expected value.
    """
    assert setup._generatorfind() == [['Clase1_1', 'Clase1_2', 'firstn'], \
        ['Clase1_1', 'Clase1_3', 'firstn'], \
        ['Clase2_1', 'Clase2_2', 'firstn'], ['primera', 'segunda', 'qsfn'], ['generator']]

def test_callsites_pruebas(setup):
    """test_callsites_pruebas will check that the calls to the generators are the expected.
    """
    assert setup.assign_call_find() ==  {('generator',): [41, 43, 44], ('Clase1_1', 'Clase1_2', 'firstn'): [49, 56, 68, 77], ('Clase1_1', 'Clase1_3', 'firstn'): [62, 64], 
('Clase2_1', 'Clase2_2', 'firstn'): [85, 89, 92, 93]}

def test_namespace_imports(setup_imports):
    """test_namespace_imports asserts that namespaces obtains the expected value with a specific
    case in which generators are in other imported files.
    """
    assert setup_imports._generatorfind() == [['folder', 'pruebas', 'Clase1_1', 'Clase1_2', 'firstn'], \
        ['folder','pruebas', 'Clase1_1', 'Clase1_3', 'firstn'], \
        ['folder','pruebas', 'Clase2_1', 'Clase2_2', 'firstn'], \
        ['folder','pruebas', 'primera', 'segunda', 'qsfn'], \
        ['folder','pruebas', 'generator']]


def test_callsites_imports(setup_imports):
    """test_callsites_imports will check that the calls to the generators are the expected with a specific
    case in which generators are in other imported files.
    """
    assert setup_imports.assign_call_find() ==  {('folder','pruebas', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}

def test_generatorfind_multiple_assign(setup_multiple_assign):
    assert setup_multiple_assign.assign_call_find() =={('Clase', 'f'):[9,11], ('Clase2', 'g'):[9,13]}

def test_generatorfind_folder(setup_folder):
    assert setup_folder.callsites()  == {\
        'pruebas.py': {('generator',): [41, 43, 44], \
        ('Clase1_1', 'Clase1_2', 'firstn'): [49, 56, 68, 77], ('Clase1_1', 'Clase1_3', 'firstn'): [62, 64], ('Clase2_1', 'Clase2_2', 'firstn'): [85, 89, 92, 93]},\
        'prueba_simple.py': {('Clase1', 'Clase2', 'f'): [7], ('f',): [7, 19, 20, 21]},\
        '__init__.py': {}}