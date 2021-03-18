import os
from typing import Generator
from typing import List
from new_model.project_file import ProjectFile


class SoftwareProject:

    files = []
    projectPath = ''
    mainFile = ''

    def __init__(self, folderPath):
        self.__checkIfFolderExists__(folderPath)
        self.projectPath = folderPath
        self.__read_folder__(folderPath)
        self.mainFile = self.files[0].getFullPath()  # must be at least one file # noqa: E501
        # print process
        print('\nGeneral project read successfully. Files in project are:\n')
        for file in self.files:
            print(file)

    def __checkIfFolderExists__(self, folderPath):
        if (not os.path.isdir(folderPath)):
            raise ValueError('The project folder does not exist: "' + folderPath + '"')

    def __read_folder__(self, folderPath):
        self.files = []
        for root, _, files in os.walk(folderPath):
            print('Reading folder ' + root + '...')

            for filename in files:
                # file_path has the full path of filename
                file_path = os.path.join(root, filename)

                # filtering made by subclasses (see template method pattern):
                if (self.__isFileAllowedInProject__(filename)):
                    projectFile = self.__createProjectFile__(filename, file_path)  # noqa: E501
                    self.files.append(projectFile)

    def __isFileAllowedInProject__(self, fileName) -> bool:
        # by default don't filter
        return True

    def __createProjectFile__(self, filename, file_path) -> ProjectFile:
        # by default create a general file
        return ProjectFile(filename, file_path)

    def getProjectSize(self) -> int:
        return len(self.files)

    def getFilesGenerator(self) -> Generator[ProjectFile, None, None]:
        for file in self.files:
            yield file

    def getFilesInProject(self) -> List[ProjectFile]:
        return self.files

    def getProjectPath(self) -> str:
        return self.projectPath

    def getMainFile(self) -> str:
        return self.mainFile

    def setMainFile(self, fileName):
        '''
            Sets the main file of the project (to process first in the search of patterns).  # noqa: E501
            The fileName is the name inside the project folder (relative to project path). # noqa: E501
        '''
        fullPath = self.projectPath + '\\' + fileName
        if (not os.path.isfile(fullPath)):
            raise ValueError('The main file does not exist: "' + fullPath + '"')
        else:
            self.mainFile = fullPath
