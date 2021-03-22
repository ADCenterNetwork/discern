from new_model.pattern_search_result import PatternSearchResult

class GeneratorSearchResult(PatternSearchResult):

    def __init__(self, arr):
        super(GeneratorSearchResult, self).__init__(arr)

    def __str__(self):
        str = ''
        for elem in self.nodeList:
            str = str + elem + ', '  # noqa: E501

        if (len(self.nodeList) > 0):
            # left the last comma out
            str = str[0:(len(str)-2)]
        return 'GeneratorSearchResult: ['+str+']'
