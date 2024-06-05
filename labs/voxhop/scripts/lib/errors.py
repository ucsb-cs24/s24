class ParseError(Exception):
    def __init__(self, line, message):
        super(ParseError, self).__init__('Parse error on line %d: %s' % (line, message))

class InvalidPoint(Exception):
    def __init__(self, point):
        super(InvalidPoint, self).__init__('Invalid point: ' + str(point))

class InvalidPath(Exception):
    def __init__(self, message):
        super(InvalidPath, self).__init__('Invalid path: ' + message)
