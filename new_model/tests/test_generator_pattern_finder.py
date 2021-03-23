import ast, sys
import os, pytest, shutil
# from generatorfind.folderCalls import FolderCalls
from new_model.generator_pattern_finder import GeneratorPatternFinder
from new_model.python_project import PythonProject
from new_model.generator_search_result import GeneratorSearchResult

tests_path = os.path.join(os.getcwd(), 'tests')

@pytest.fixture
def finderPruebas():
    project = PythonProject(tests_path)
    project.setMainFile('pruebas.py')
    finder = GeneratorPatternFinder(project)
    return finder

@pytest.fixture
def finderPruebas2():
    project = PythonProject(tests_path)
    project.setMainFile('pruebas2.py')
    finder = GeneratorPatternFinder(project)
    return finder
    # prueba_imports = GeneratorPatternFinder(path_imports, [os.path.abspath("tests\\folder\\pruebas.py")])
    # return prueba_imports

@pytest.fixture
def finderPruebas4():
    project = PythonProject(tests_path)
    project.setMainFile('pruebas4.py')
    finder = GeneratorPatternFinder(project)
    return finder
    # path_imports = os.path.join(os.getcwd(), 'tests', 'pruebas4.py')
    # prueba_imports = GeneratorPatternFinder(path_imports, [os.path.abspath("tests\\folder\\pruebas.py")])
    # return prueba_imports

@pytest.fixture
def setup_multiple_assign():
    project = PythonProject(tests_path)
    project.setMainFile('multiple_assign.py')
    finder = GeneratorPatternFinder(project)
    return finder

@pytest.fixture
def setup_discern2_importpackage():
    project = PythonProject(tests_path)
    project.setMainFile('pruebas3.py')
    finder = GeneratorPatternFinder(project)
    return finder
    # path = os.path.join(os.getcwd(), 'tests', 'pruebas3.py')
    # prueba = GeneratorPatternFinder(path, [os.path.abspath("tests\\folder")])
    # return prueba

# @pytest.fixture
# def setup_discern2_pruebas2():
#     path = os.path.join(os.getcwd(), 'tests', 'pruebas2.py')
#     prueba = GeneratorPatternFinder(path, [os.path.abspath("tests\\folder\\pruebas.py")])
#     return prueba

@pytest.fixture
def setup_pruebas_assign():
    project = PythonProject(tests_path)
    project.setMainFile('pruebas_assign.py')
    finder = GeneratorPatternFinder(project)
    return finder

# @pytest.fixture
# def setup_discern2_relativeimports():
#     path = os.path.join(os.getcwd(), 'tests', 'folder', 'relativeimports.py')
#     prueba = GeneratorPatternFinder(path, [os.path.abspath("tests\\ejemplo\\prueba_simple.py")])
#     return prueba


def test_namespace_pruebas(finderPruebas):
    """test_namespace_pruebas asserts that namespaces obtains the expected value on a simple file.
    """
    result = finderPruebas.findPatterns()
    
    assert len(result) == 5
    
    expected = []
    expected.append( GeneratorSearchResult(['Clase1_1', 'Clase1_2', 'firstn']) )
    expected.append( GeneratorSearchResult(['Clase1_1', 'Clase1_3', 'firstn']) )
    expected.append( GeneratorSearchResult(['Clase2_1', 'Clase2_2', 'firstn']) )
    expected.append( GeneratorSearchResult(['primera', 'segunda', 'qsfn']) )
    expected.append( GeneratorSearchResult(['generator']) )

    for i in range(5):
        # compare the real results with expected
        assert result[i] == expected[i]

def test_namespace_pruebas_assign(setup_pruebas_assign):
    """test_namespace_pruebas asserts that namespaces obtains the expected value on a simple file.
    """
    result = setup_pruebas_assign.findPatterns()
    
    assert result[0] == GeneratorSearchResult(['Clase1', 'funcion'])

def test_namespace_imports(finderPruebas2):
    """ test_namespace_imports asserts that namespaces obtains the expected value with a specific
    case in which generators are in other imported files.
    """
    result = finderPruebas2.findPatterns()
    
    expected = []
    
    expected.append( GeneratorSearchResult(['folder', 'pruebas', 'Clase1_1', 'Clase1_2', 'firstn']) )
    expected.append( GeneratorSearchResult(['folder','pruebas', 'Clase1_1', 'Clase1_3', 'firstn']) )
    expected.append( GeneratorSearchResult(['folder','pruebas', 'Clase2_1', 'Clase2_2', 'firstn']) )
    expected.append( GeneratorSearchResult(['folder','pruebas', 'primera', 'segunda', 'qsfn']) )
    expected.append( GeneratorSearchResult(['folder','pruebas', 'generator']) )

    for i in range(5):
        # compare the real results with expected
        assert result[i] == expected[i]

def test_relativeimports(setup_discern2_relativeimports):
    """test_namespace_imports asserts that namespaces obtains the expected value with a specific
    case in which generators are in other imported files.
    """
    result = setup_discern2_relativeimports.findPatterns()
    
    expected = []
    expected.append( GeneratorSearchResult(['prueba_simple', 'Clase1', 'Clase2', 'f']))
    expected.append( GeneratorSearchResult(['prueba_simple', 'f']))

    for i in range(2):
        # compare the real results with expected
        assert result[i] == expected[i]