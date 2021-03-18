from typing import List
from new_model.pattern_search_result import PatternSearchResult
from new_model.abstract_pattern_finder import AbstractPatternFinder


class DecoratorPatternFinder(AbstractPatternFinder):

    def __init__(self, softwareProject):
        pass

    def findPatterns(self) -> List[PatternSearchResult]:
        return []
