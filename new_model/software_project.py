import os
from typing import Generator
from new_model.project_file import ProjectFile


class SoftwareProject:

    files = []

    def __init__(self, folderPath):
        self.__read_folder__(folderPath)
        print('\nGeneral project read successfully. Files in project are:\n')
        for file in self.files:
            print(file)

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

    def getFilesIterator(self) -> Generator[ProjectFile, None, None]:
        for file in self.files:
            yield file
