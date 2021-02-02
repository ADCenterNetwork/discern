from get_repos import parse_urls_from_text, download_repos
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


def test_parse_urls_from_text():
    assert parse_urls_from_text("https://github.com/devonfw/devon4ng\n    \ndevonfw/devon4j/     \n  devonfw/devon4j    \n https://github.com/devonfw/devon4ng/ ") == ["https://github.com/devonfw/devon4ng", "https://github.com/devonfw/devon4j", "https://github.com/devonfw/devon4j", "https://github.com/devonfw/devon4ng"] 

def test_download_repo(workspace):
    res = download_repos(['https://github.com/devonfw/getting-started', 'https://github.com/sldkfjsdlkfjsldf/sdkjflksjdf'], workspace)    
    assert len(res) == 1
    assert os.path.isfile(os.path.join(workspace, 'getting-started/devonfw_getting_started.pdf')) == True 
    assert os.path.isfile(os.path.join(workspace, 'sdkjflksjdf')) == False

