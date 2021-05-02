class Token:
    TK_IDENTIFIER     = 0
    TK_SPECIAL_CHAR   = 1
    TK_RESERVED_WORD  = 2
    TK_INT            = 3
    TK_FLOAT          = 4
    TK_ARITHMETIC_OPERATOR = 5
    TK_RELATIONAL_OPERATOR = 6
    TK_ASSIGNMENT_OPERATOR = 7
    TK_CHAR = 8

    def __init__(self, tokenType, text, line, column):
        self.type = tokenType
        self.text = text
        self.line = line
        self.column = column
    
    def getType(self):
        if (self.type is self.TK_IDENTIFIER):
            tokenType = 'Identifier'
        if (self.type is self.TK_SPECIAL_CHAR):
            tokenType = 'Special Character'
        if (self.type is self.TK_RESERVED_WORD):
            tokenType = 'Reserved Word'
        elif (self.type is self.TK_INT):
            tokenType = 'Integer'
        elif (self.type is self.TK_FLOAT):
            tokenType = 'Float'
        elif (self.type is self.TK_ARITHMETIC_OPERATOR):
            tokenType = 'Arithmetic Operator'
        elif (self.type is self.TK_RELATIONAL_OPERATOR):
            tokenType = 'Relational Operator'
        elif (self.type is self.TK_ASSIGNMENT_OPERATOR):
            tokenType = 'Assignment Operator'
        elif (self.type is self.TK_CHAR):
            tokenType = 'Char'
        return tokenType

    def __repr__(self):
        return 'Token [Type: ' + self.getType() + ' | Text: ' + self.text + ' | Line: ' + str(self.line) + ' | Column: ' + str(self.column) + ']'
