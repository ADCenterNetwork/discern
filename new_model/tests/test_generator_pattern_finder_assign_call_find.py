import os, pytest
from new_model.generator_pattern_finder import GeneratorPatternFinder
from new_model.python_project import PythonProject

tests_path = os.path.join(os.getcwd(), 'tests')


@pytest.fixture
def finderPruebas2():
    project = PythonProject(tests_path)
    project.setMainFile('pruebas2.py')
    finder = GeneratorPatternFinder(project)
    return finder

def test_callsites_imports(finderPruebas2):
    calls = finderPruebas2.findCalls()
    
    assert calls ==  {('folder','pruebas', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}

