from tests import folder
from discern_fwk.software_project.python_file import PythonFile
from discern_fwk.software_project.software_project import SoftwareProject


class PythonProject(SoftwareProject):

    def __init__(self, folderPath):
        super(PythonProject, self).__init__(folderPath)

    def __isFileAllowedInProject__(self, fileName) -> bool:
        # filter by extension "py"
        return fileName.endswith('.py')

    def __createProjectFile__(self, filename, file_path) -> PythonFile:
        # creates a PythonFile
        return PythonFile(filename, file_path)
