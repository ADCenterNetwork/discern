import os
from new_model.project_file import ProjectFile


class SoftwareProject:

    files = []

    def __init__(self, folderPath):
        self.__read_folder__(folderPath)
        print('\nProject read successfully. Files in project include:\n')
        for file in self.files:
            print(file)

    def __read_folder__(self, folderPath):
        self.files = []
        for root, _, files in os.walk(folderPath):
            print('Reading folder ' + root + '...')

            for filename in files:
                file_path = os.path.join(root, filename)

                # print('\t- file %s (full path: %s)' % (filename, file_path))
                if (filename.endswith('.py')):
                    projectFile = ProjectFile(filename, file_path, 'Python')
                    self.files.append(projectFile)
