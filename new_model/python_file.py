from new_model.project_file import ProjectFile
import os


class PythonFile(ProjectFile):

    def __init__(self, fileName, fullPath):
        if (not fileName.endswith('.py')):
            raise ValueError('Only python files allowed.')
        if (not os.path.isfile(fullPath)):
            raise ValueError('File path does not exist: ' + fullPath)
        self.fileName = fileName
        self.fullPath = fullPath

    def __str__(self) -> str:
        return 'PythonFile: ' + self.fullPath

    def getFileType(self) -> str:
        return 'Python'
