from typing import List
from . import PatternSearchResult
from . import SoftwareProject
from . import DecoratorPatternFinder
from . import ObserverPatternFinder
from . import GeneratorPatternFinder


class PatternFinderMain():
    '''
    This is the main class for pattern search

    '''
    def findPatterns(self, path) -> List[PatternSearchResult]:
        '''
        This is the main entry point for the process of finding patterns
        in this framework.
        '''
        project = SoftwareProject(path)

        # new implementations should be added here:
        searchImplementations = [GeneratorPatternFinder(),
                                 ObserverPatternFinder(),
                                 DecoratorPatternFinder()]
        results = []

        # for each implementation, search for pattern instances on the project
        for finder in searchImplementations:
            results.append(finder.findPatterns(project))

        return results
