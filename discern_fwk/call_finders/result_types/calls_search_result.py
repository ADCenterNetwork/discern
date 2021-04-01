from discern_fwk.pattern_finders.result_types.process_result import ProcessResult


class CallsSearchResult(ProcessResult):

    # This is a dictionary with the names of the files and the matches found in each of them
    filesDict = {}

    def __init__(self, callsDictionary = None):
        if (callsDictionary == None):
            self.filesDict = {}
        else:
            self.filesDict = callsDictionary

    def setPatternCallsForFile(self, filename, callsDict):
        self.filesDict[filename] = callsDict
    
    def getPatternCallsForFile(self, filename):
        return self.filesDict[filename]

    def __eq__(self, other): 
        if not isinstance(other, CallsSearchResult):
            return False

        return self.filesDict == other.filesDict

    