import os, pytest
from new_model.generator_pattern_finder import GeneratorPatternFinder
from new_model.python_project import PythonProject

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

@pytest.fixture
def finderPruebas4():
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
def setup_folder():
    folder_path = os.path.join(os.getcwd(), 'tests', 'folder')
    project = PythonProject(folder_path)
    finder = GeneratorPatternFinder(project)
    return finder
    
@pytest.fixture
def setupPruebas3():
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
    folder_path = os.path.join(os.getcwd(), 'tests', 'folder')
    project = PythonProject(folder_path)
    project.setMainFile('relativeimports.py')
    finder = GeneratorPatternFinder(project)
    return finder


def test_callsites_imports(finderPruebas2):
    calls = finderPruebas2.findCalls()

    assert calls ==  {('folder','pruebas', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}

def test_callsites_pruebas(finderPruebas):
    """test_callsites_pruebas will check that the calls to the generators are the expected on a simple file.
    """
    calls = finderPruebas.findCalls()
    assert calls ==  {('generator',): [41, 43, 44], ('Clase1_1', 'Clase1_2', 'firstn'): [49, 56, 68, 70, 77], ('Clase1_1', 'Clase1_3', 'firstn'): [62, 64], 
('Clase2_1', 'Clase2_2', 'firstn'): [85, 89, 92, 93]}

def test_callsites_pruebas_assign(setup_pruebas_assign):
    """test_callsites_pruebas will check that the calls to the generators are the expected on a simple file.
    """
    calls = setup_pruebas_assign.findCalls()
    assert calls ==  {('Clase1', 'funcion'): [8, 10]}

def test_callsites_imports(finderPruebas2):
    """test_callsites_imports will check that the calls to the generators are the expected with a specific
    case in which generators are in other imported files.
    """
    calls = finderPruebas2.findCalls()
    assert calls ==  {('folder','pruebas', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}

def test_callsites_importfrom(finderPruebas4):
    """test_callsites_importfrom will check that the calls to the generators are the expected with a specific
    case in which generators are imported with ImportFrom statements.
    """
    calls = finderPruebas4.findCalls()
    assert calls ==  {('pruebas', 'Clase1_1', 'Clase1_2', 'firstn'): [4]}

def test_generatorfind_multiple_assign(setup_multiple_assign):
    """test_generatorfind_multiple_assign will check that discern works succesfully with multiple
    imports of generators at the same line.
    """
    assert setup_multiple_assign.findCalls() =={('Clase', 'f'):[9,11], ('Clase2', 'g'):[9,13]}

def test_generatorfind_folder(setup_folder):
    """We input a folder, 
    and the software will give us the namespace of the generators on the python files 
    inside the input folder.
    """
    assert setup_folder.findCalls()  == {'pruebas.py': {('generator',): [41, 43, 44], ('Clase1_1', 'Clase1_2', 'firstn'): [49, 56, 68, 70, 77], ('Clase1_1', 'Clase1_3', 'firstn'): [62, 64], ('Clase2_1', 'Clase2_2', 'firstn'): [85, 89, 92, 93]}, 'prueba_simple.py': {('Clase1', 'Clase2', 'f'): [7], ('f',): [7, 19, 20, 21]}}

def test_discern_callsites_pruebas2(finderPruebas2):
    """test_discern_callsites_pruebas2 will check that the calls to the generators are the expected with a specific
    case in which generators are in other imported files.
    """
    assert finderPruebas2.findCalls() ==  {('folder','pruebas', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}

def test_discern_importpackage(setupPruebas3):
    """test_discern_importpackage will check that the calls to the generators are the expected with a specific
    case in which generators are in an imported package with his own namespaces. Also, in that file we have another 
    imported file without interest in search generators, so we do not try to detect generators in that file.
    """
    assert setupPruebas3.findCalls() ==  {('folder', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}
