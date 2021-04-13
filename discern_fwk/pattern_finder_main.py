import time
from typing import List
from discern_fwk.pattern_finders.result_types.pattern_search_result import PatternSearchResult
from discern_fwk.software_project.python_project import PythonProject
from discern_fwk.pattern_finders.decorator_pattern_finder import DecoratorPatternFinder
from discern_fwk.pattern_finders.observer_pattern_finder import ObserverPatternFinder
from discern_fwk.pattern_finders.generator_pattern_finder import GeneratorPatternFinder


class PatternFinderMain():
    '''
    This is the main class for pattern search

    '''
    @classmethod
    def findPatterns(cls, path, mainFile='') -> List[PatternSearchResult]:
        '''
        This is the main entry point for the process of finding patterns
        in this framework.

        path: must be a folder in the filesystem, where the file, project or
              folder structure is located.
        mainFile: by default, the project sets the first file as main file.
                  If this parameter is passed, the main file for the project
                  is set, where the patterns are searched for.
        '''
        start = time.time()
        project = PythonProject(path)

        if (mainFile != ''):
            project.setMainFile(mainFile)

        # new implementations should be added here:
        searchImplementations = [GeneratorPatternFinder(project),
                                 ObserverPatternFinder(project),
                                 DecoratorPatternFinder(project)]
        results = []

        # for each implementation, search for pattern instances on the project
        for finder in searchImplementations:
            results = results + finder.findPatterns()  # concat results for finder pattern # noqa: E501

        print('\n' + str(len(results)) + ' pattern instances found:\n')
        for result in results:
            print(result)

        PatternFinderMain.printExecTime(start)
        return results

    @classmethod
    def printExecTime(cls, start):
        end = time.time()
        print('-----------------------------------------------------------------------------------------------------')  # noqa: E501
        tiempoej = end-start
        if tiempoej > 60:
            tiempoejmin = tiempoej // 60
            tiempoejsec = tiempoej % 60
            print('Execution time:', tiempoejmin, 'min and ', tiempoejsec,  'seconds.')  # noqa: E501
        else:
            print('Execution time:', end-start, 'seconds.')
        print('-----------------------------------------------------------------------------------------------------')  # noqa: E501
