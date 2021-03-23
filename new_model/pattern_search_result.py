from new_model.process_result import ProcessResult


class PatternSearchResult(ProcessResult):

    nodeList = []

    def __init__(self, arr):
        self.nodeList = arr

    def __eq__(self, other): 
        if not isinstance(other, PatternSearchResult):
            return False

        equal = True
        i = 0
        for str in self.nodeList:
            # compare strings
            equal = equal and (str == other.nodeList[i])
            i = i + 1
        return equal


    def __str__(self):
        str = ''
        for elem in self.nodeList:
            str = str + elem + ', '  # noqa: E501

        if (len(self.nodeList) > 0):
            # left the last comma out
            str = str[0:(len(str)-2)]
        return 'PatternSearchResult: ['+str+']'
