from typing import List
from discern_fwk.call_finders.result_types.calls_search_result import CallsSearchResult


class AbstractCallsFinder:

    def __init__(self, pattern_finder):
        pass

    def findPatternCalls(self) -> List[CallsSearchResult]:
        pass