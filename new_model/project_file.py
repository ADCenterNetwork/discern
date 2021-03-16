

class ProjectFile:

    fileName = ''
    fullPath = ''
    fileType = ''

    def __init__(self, fileName, fullPath, fileType):
        self.fileName = fileName
        self.fullPath = fullPath
        self.fileType = fileType

    def __str__(self) -> str:
        return 'ProjectFile: ' + self.fullPath
