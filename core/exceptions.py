class FormException(Exception):
    def __init(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class NetworkException(Exception):
    def __init(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ParserException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class SpiderException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
