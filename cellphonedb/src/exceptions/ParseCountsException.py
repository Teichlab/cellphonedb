class ParseCountsException(Exception):
    def __init__(self):
        super(ParseCountsException, self).__init__('Error parsing Counts data')
