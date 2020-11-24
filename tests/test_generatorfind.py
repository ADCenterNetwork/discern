from ..generatorfind.generatorfind import Code
import ast
import os, pytest, shutil


@pytest.fixture
def setup():
    path = os.path.join(os.getcwd(), 'tests', 'pruebas.py')
    prueba = Code(path)
    return prueba

@pytest.fixture
def setup2():
    path2 = os.path.join(os.getcwd(), 'tests', 'pruebas2.py')
    prueba2 = Code(path2)
    return prueba2


def test_generatorfind(setup):
    """test_generatorfind asserts that namespaces obtains the expected value.
    """
    assert setup.generatorfind() == [['Clase1_1', 'Clase1_2', 'firstn'], \
        ['Clase1_1', 'Clase1_3', 'firstn'], \
        ['Clase2_1', 'Clase2_2', 'firstn'], ['primera', 'segunda', 'qsfn'], ['generator']]

def test_assign_call_find(setup):
    """test_2assign_call_find will check that the calls to the generators are the expected.
    """

    assert setup.assign_call_find() ==  {('generator',): [41, 43, 44], ('Clase1_1', 'Clase1_2', 'firstn'): [49, 56, 68, 77], ('Clase1_1', 'Clase1_3', 'firstn'): [62, 64], 
('Clase2_1', 'Clase2_2', 'firstn'): [85, 89, 92, 93]}


def test_generatorfind2(setup2):
    """test_generatorfind2 asserts that namespaces2 obtains the expected value.
    """
    assert setup2.generatorfind() == [['pruebas', 'Clase1_1', 'Clase1_2', 'firstn'], \
        ['pruebas', 'Clase1_1', 'Clase1_3', 'firstn'], \
        ['pruebas', 'Clase2_1', 'Clase2_2', 'firstn'], \
        ['pruebas', 'primera', 'segunda', 'qsfn'], \
        ['pruebas', 'generator'], \
        ['prueba_simple', 'Clase1', 'Clase2', 'f'], \
        ['prueba_simple', 'f']]

def test_assign_call_find2(setup2):
    """test_2assign_call_find will check that the calls to the generators are the expected.
    """

    assert setup2.assign_call_find() ==  {('pruebas', 'Clase1_1', 'Clase1_2', 'firstn'): [3]}