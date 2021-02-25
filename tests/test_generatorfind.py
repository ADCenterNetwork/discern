import ast, sys
import os, pytest, shutil

#print(sys.path)
#print(os.getcwd())
from generatorfind.folderCalls import FolderCalls
from generatorfind.discern2 import Discern2






@pytest.fixture
def setup():
    path = os.path.join(os.getcwd(), 'tests', 'pruebas.py')
    prueba = Discern2(path, [])
    return prueba

@pytest.fixture
def setup_imports():
    path_imports = os.path.join(os.getcwd(), 'tests', 'pruebas2.py')
    prueba_imports = Discern2(path_imports, [os.path.abspath("tests\\folder\\pruebas.py")])
    return prueba_imports

@pytest.fixture
def setup_importfrom():
    path_imports = os.path.join(os.getcwd(), 'tests', 'pruebas4.py')
    prueba_imports = Discern2(path_imports, [os.path.abspath("tests\\folder\\pruebas.py")])
    return prueba_imports


@pytest.fixture
def setup_multiple_assign():
    path = os.path.join(os.getcwd(), 'tests', 'multiple_assign.py')
    prueba = Discern2(path, [])
    return prueba

@pytest.fixture
def setup_folder():
    path = os.path.join(os.getcwd(), 'tests', 'folder')
    prueba = FolderCalls(path)
    return prueba

@pytest.fixture
def setup_discern2_importpackage():
    path = os.path.join(os.getcwd(), 'tests', 'pruebas3.py')
    prueba = Discern2(path, [os.path.abspath("tests\\folder")])
    return prueba

@pytest.fixture
def setup_discern2_pruebas2():
    path = os.path.join(os.getcwd(), 'tests', 'pruebas2.py')
    prueba = Discern2(path, [os.path.abspath("tests\\folder\\pruebas.py")])
    return prueba

@pytest.fixture
def setup_pruebas_assign():
    path = os.path.join(os.getcwd(), 'tests', 'pruebas_assign.py')
    prueba = Discern2(path, [])
    return prueba

@pytest.fixture
def setup_discern2_relativeimports():
    path = os.path.join(os.getcwd(), 'tests', 'folder', 'relativeimports.py')
    prueba = Discern2(path, [os.path.abspath("tests\\ejemplo\\prueba_simple.py")])
    return prueba


def test_namespace_pruebas(setup):
    """test_namespace_pruebas asserts that namespaces obtains the expected value on a simple file.
    """
    assert setup._generatorfind() == [['Clase1_1', 'Clase1_2', 'firstn'], \
        ['Clase1_1', 'Clase1_3', 'firstn'], \
        ['Clase2_1', 'Clase2_2', 'firstn'], ['primera', 'segunda', 'qsfn'], ['generator']]

def test_callsites_pruebas(setup):
    """test_callsites_pruebas will check that the calls to the generators are the expected on a simple file.
    """
    assert setup.assign_call_find() ==  {('generator',): [41, 43, 44], ('Clase1_1', 'Clase1_2', 'firstn'): [49, 56, 68, 70, 77], ('Clase1_1', 'Clase1_3', 'firstn'): [62, 64], 
('Clase2_1', 'Clase2_2', 'firstn'): [85, 89, 92, 93]}

def test_namespace_pruebas_assign(setup_pruebas_assign):
    """test_namespace_pruebas asserts that namespaces obtains the expected value on a simple file.
    """
    assert setup_pruebas_assign._generatorfind() == [['Clase1', 'funcion']]

def test_callsites_pruebas_assign(setup_pruebas_assign):
    """test_callsites_pruebas will check that the calls to the generators are the expected on a simple file.
    """
    assert setup_pruebas_assign.assign_call_find() ==  {('Clase1', 'funcion'): [8, 10]}

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

def test_callsites_importfrom(setup_importfrom):
    """test_callsites_importfrom will check that the calls to the generators are the expected with a specific
    case in which generators are imported with ImportFrom statements.
    """
    assert setup_importfrom.assign_call_find() ==  {('pruebas', 'Clase1_1', 'Clase1_2', 'firstn'): [4]}
def test_generatorfind_multiple_assign(setup_multiple_assign):
    """test_generatorfind_multiple_assign will check that discern works succesfully with multiple
    imports of generators at the same line.
    """
    assert setup_multiple_assign.assign_call_find() =={('Clase', 'f'):[9,11], ('Clase2', 'g'):[9,13]}

def test_generatorfind_folder(setup_folder):
    """We input a folder, 
    and the software will give us the namespace of the generators on the python files 
    inside the input folder.
    """
    assert setup_folder.callsites()  == {'pruebas.py': {('generator',): [41, 43, 44], ('Clase1_1', 'Clase1_2', 'firstn'): [49, 56, 68, 70, 77], ('Clase1_1', 'Clase1_3', 'firstn'): [62, 64], ('Clase2_1', 'Clase2_2', 'firstn'): [85, 89, 92, 93]}, 'prueba_simple.py': {('Clase1', 'Clase2', 'f'): [7], ('f',): [7, 19, 20, 21]}}

def test_discern_callsites_pruebas2(setup_discern2_pruebas2):
    """test_discern_callsites_pruebas2 will check that the calls to the generators are the expected with a specific
    case in which generators are in other imported files.
    """
    assert setup_discern2_pruebas2.assign_call_find() ==  {('folder','pruebas', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}

def test_discern_importpackage(setup_discern2_importpackage):
    """test_discern_importpackage will check that the calls to the generators are the expected with a specific
    case in which generators are in an imported package with his own namespaces. Also, in that file we have another 
    imported file without interest in search generators, so we do not try to detect generators in that file.
    """
    assert setup_discern2_importpackage.assign_call_find() ==  {('folder', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}

def test_relativeimports(setup_discern2_relativeimports):
    """test_namespace_imports asserts that namespaces obtains the expected value with a specific
    case in which generators are in other imported files.
    """
    assert setup_discern2_relativeimports._generatorfind() == [['prueba_simple', 'Clase1', 'Clase2', 'f'], ['prueba_simple', 'f']]