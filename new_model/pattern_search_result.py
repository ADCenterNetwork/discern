from new_model.process_result import ProcessResult


class PatternSearchResult(ProcessResult):

    nodeList = []

    def __init__(self, arr):
        self.nodeList = arr

    def __str__(self):
        str = ''
        for elem in self.nodeList:
            str = str + elem + ', '  # noqa: E501

        if (len(self.nodeList) > 0):
            # left the last comma out
            str = str[0:(len(str)-2)]
        return 'PatternSearchResult: ['+str+']'
