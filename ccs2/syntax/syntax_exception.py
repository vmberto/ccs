class SyntaxException(Exception):
    def __init__(self, msg, token = None):
        if (token):
            Exception.__init__(self, 
                'Syntax Error: ' + msg  
                + (', found ' + token.getType() 
                + ' ( ' + token.text + ' ) at LINE ' + str(token.line) 
                + ' and COLUMN ' + str(token.column))
            )
        else:
            Exception.__init__(self, 'Syntax Error: ' + msg)