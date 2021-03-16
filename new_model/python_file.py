from new_model.project_file import ProjectFile


class PythonFile(ProjectFile):

    def __init__(self, fileName, fullPath):
        if (not fileName.endswith('.py')):
            raise ValueError('Only python files allowed.')
        self.fileName = fileName
        self.fullPath = fullPath

    def __str__(self) -> str:
        return 'PythonFile: ' + self.fullPath

    def getFileType() -> str:
        return 'Python'
