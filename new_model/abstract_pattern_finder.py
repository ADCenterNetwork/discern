from typing import List
from new_model.pattern_search_result import PatternSearchResult


class AbstractPatternFinder:

    def __init__(self):
        pass

    def findPatterns(self, softwareProject) -> List[PatternSearchResult]:
        pass