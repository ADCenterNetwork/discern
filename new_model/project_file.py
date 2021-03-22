import io
import ast

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

    def getFullPath(self) -> str:
        return self.fullPath

    def getNodeForFile(self):
        file = io.open(self.getFullPath(), encoding="iso-8859-15", errors='ignore')
        astNode = ast.parse(file.read())
        file.close()
        return astNode