from typing import List
from new_model.pattern_search_result import PatternSearchResult
from new_model.python_project import PythonProject
from new_model.decorator_pattern_finder import DecoratorPatternFinder
from new_model.observer_pattern_finder import ObserverPatternFinder
from new_model.generator_pattern_finder import GeneratorPatternFinder


class PatternFinderMain():
    '''
    This is the main class for pattern search

    '''
    def findPatterns(self, path) -> List[PatternSearchResult]:
        '''
        This is the main entry point for the process of finding patterns
        in this framework.
        '''
        project = PythonProject(path)

        # new implementations should be added here:
        searchImplementations = [GeneratorPatternFinder(),
                                 ObserverPatternFinder(),
                                 DecoratorPatternFinder()]
        results = []

        # for each implementation, search for pattern instances on the project
        for finder in searchImplementations:
            results = results + finder.findPatterns(project)  # concat results for finder pattern # noqa: E501

        print(str(len(results)) + ' pattern instances found:\n')
        for result in results:
            print(result)

        return results
