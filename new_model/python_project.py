from tests import folder
from new_model.python_file import PythonFile
from new_model.software_project import SoftwareProject


class PythonProject(SoftwareProject):

    def __init__(self, folderPath):
        # self.__read_folder__(folderPath)
        # print('\nPython project read successfully. Files in project are:\n')
        # for file in self.files:
        #     print(file)
        super(PythonProject, self).__init__(folderPath)

    def __isFileAllowedInProject__(self, fileName) -> bool:
        # filter by extension "py"
        return fileName.endswith('.py')

    def __createProjectFile__(self, filename, file_path) -> PythonFile:
        # creates a PythonFile
        return PythonFile(filename, file_path)
