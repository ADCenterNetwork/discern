from typing import List
from discern_fwk.pattern_finders.result_types.pattern_search_result import PatternSearchResult
from discern_fwk.pattern_finders.abstract_pattern_finder import AbstractPatternFinder


class ObserverPatternFinder(AbstractPatternFinder):

    def __init__(self, softwareProject):
        pass

    def findPatterns(self) -> List[PatternSearchResult]:
        return []
