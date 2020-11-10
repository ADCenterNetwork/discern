from generatorfind import Code
import ast
import os, pytest, shutil

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    From https://stackoverflow.com/a/2656405

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise Exception("Cannot delete dir with shutil.rmtree")

@pytest.fixture
def workspace():
    path = os.path.join(os.getcwd(), '__downloaded__')
    if not os.path.isdir(path):
        os.mkdir(path)
    yield path  
    try:
        shutil.rmtree(path, onerror=onerror)
    except Exception as ex:
        print(ex)


path = os.path.join(os.getcwd(), 'tests', 'pruebas.py')
prueba = Code(path)

yieldfind = prueba.yieldfind
generatorfind = prueba.generatorfind
assignsearch = prueba.assignsearch
findcall = prueba.findcall




def test_generatorfind():
    yieldfind()
    generatorfind()
    assert prueba.generators == [['Clase1_1', 'Clase1_2', 'firstn'], ['Clase2_1', 'Clase2_2', 'firstn'], ['primera', 'segunda', 'qsfn'], ['generator']]
