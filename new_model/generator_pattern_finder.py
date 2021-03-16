from typing import List
from new_model.pattern_search_result import PatternSearchResult
from new_model.abstract_pattern_finder import AbstractPatternFinder


class GeneratorPatternFinder(AbstractPatternFinder):

    def findPatterns(self, softwareProject) -> List[PatternSearchResult]:
        return []
