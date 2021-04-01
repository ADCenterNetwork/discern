from typing import List
from discern_fwk.pattern_finders.result_types.pattern_search_result import PatternSearchResult


class AbstractPatternFinder:

    def __init__(self):
        pass

    def findPatterns(self) -> List[PatternSearchResult]:
        pass