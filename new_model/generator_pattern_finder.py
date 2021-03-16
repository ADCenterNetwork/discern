from types import List
from . import PatternSearchResult
from . import AbstractPatternFinder


class GeneratorPatternFinder(AbstractPatternFinder):

    def findPattern(self, softwareProject) -> List[PatternSearchResult]:
        return []
