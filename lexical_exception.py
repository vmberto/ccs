class LexicalException(Exception):
    def __init__(self, msg):
            Exception.__init__(self, 'Lexical Error: ' + msg)