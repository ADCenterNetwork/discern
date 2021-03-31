import ast, sys
import os, pytest, shutil
# from generatorfind.folderCalls import FolderCalls
from new_model.generator_pattern_finder import GeneratorPatternFinder
from new_model.python_project import PythonProject
from new_model.generator_search_result import GeneratorSearchResult

tests_path = os.path.join(os.getcwd(), 'tests')


@pytest.fixture
def finderPruebas_gen_and_call():
    project = PythonProject(tests_path)
    project.setMainFile('pruebas.py')
    finder = GeneratorPatternFinder(project)
    return finder


@pytest.fixture
def finderPruebas2_import():
    project = PythonProject(tests_path)
    project.setMainFile('pruebas2.py')
    finder = GeneratorPatternFinder(project)
    return finder


@pytest.fixture
def finderPruebas4_importfrom():
    project = PythonProject(tests_path)
    project.setMainFile('pruebas4.py')
    finder = GeneratorPatternFinder(project)
    return finder


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

@pytest.fixture
def setup_pruebas_assign():
    project = PythonProject(tests_path)
    project.setMainFile('pruebas_assign.py')
    finder = GeneratorPatternFinder(project)
    return finder


@pytest.fixture
def setup_discern2_relativeimports():
    path = os.path.join(tests_path)
    project = PythonProject(path)
    project.setMainFile('folder\\relativeimports.py')
    finder = GeneratorPatternFinder(project)
    return finder


def test_namespace_pruebas(finderPruebas_gen_and_call):
    """test_namespace_pruebas asserts that namespaces obtains the expected value on a simple file.   # noqa: E501
    """
    result = finderPruebas_gen_and_call.findPatterns()

    assert len(result) == 5

    expected = []
    expected.append(GeneratorSearchResult(['Clase1_1', 'Clase1_2', 'firstn']))
    expected.append(GeneratorSearchResult(['Clase1_1', 'Clase1_3', 'firstn']))
    expected.append(GeneratorSearchResult(['Clase2_1', 'Clase2_2', 'firstn']))
    expected.append(GeneratorSearchResult(['primera', 'segunda', 'qsfn']))
    expected.append(GeneratorSearchResult(['generator']))

    for i in range(5):
        # compare the real results with expected
        assert result[i] == expected[i]


def test_namespace_pruebas_assign(setup_pruebas_assign):
    """test_namespace_pruebas asserts that namespaces obtains the expected value on a simple file.   # noqa: E501
    """
    result = setup_pruebas_assign.findPatterns()

    assert result[0] == GeneratorSearchResult(['Clase1', 'funcion'])


def test_namespace_imports(finderPruebas2_import):
    """ test_namespace_imports asserts that namespaces obtains the expected value with a specific   # noqa: E501
    case in which generators are in other imported files.
    """
    result = finderPruebas2_import.findPatterns()
    print(result)
    expected = []

    expected.append(GeneratorSearchResult(['folder', 'pruebas', 'Clase1_1', 'Clase1_2', 'firstn']))   # noqa: E501
    expected.append(GeneratorSearchResult(['folder', 'pruebas', 'Clase1_1', 'Clase1_3', 'firstn']))   # noqa: E501
    expected.append(GeneratorSearchResult(['folder', 'pruebas', 'Clase2_1', 'Clase2_2', 'firstn']))   # noqa: E501
    expected.append(GeneratorSearchResult(['folder', 'pruebas', 'primera', 'segunda', 'qsfn']))   # noqa: E501
    expected.append(GeneratorSearchResult(['folder', 'pruebas', 'generator']))   # noqa: E501

    for i in range(5):
        # compare the real results with expected
        assert result[i] == expected[i]


def test_relativeimports(setup_discern2_relativeimports):
    """test_namespace_imports asserts that namespaces obtains the expected value with a specific   # noqa: E501
    case in which generators are in other imported files.
    """
    result = setup_discern2_relativeimports.findPatterns()

    expected = []
    expected.append(GeneratorSearchResult(['prueba_simple_ejemplo', 'Clase1', 'Clase2', 'f']))   # noqa: E501
    expected.append(GeneratorSearchResult(['prueba_simple_ejemplo', 'f']))
    assert len(result) == 2
    for i in range(2):
        # compare the real results with expected
        assert result[i] == expected[i]
