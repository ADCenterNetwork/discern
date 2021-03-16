

class ProjectFile:

    fileName = ''
    fullPath = ''

    def __init__(self, fileName, fullPath):
        self.fileName = fileName
        self.fullPath = fullPath

    def __str__(self) -> str:
        return 'ProjectFile: ' + self.fullPath

    def getFileType() -> str:
        return 'General file'
