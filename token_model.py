class Token:
    TK_IDENTIFIER     = 0
    TK_SPECIAL_CHAR   = 1
    TK_RESERVED_WORD  = 2
    TK_INT            = 3
    TK_FLOAT          = 4
    TK_ARITHMETIC_OPERATOR = 5
    TK_RELATIONAL_OPERATOR = 6
    TK_CHAR = 7

    def __init__(self, tokenType, text, line, column):
        self.type = tokenType
        self.text = text
        self.line = line
        self.column = column
    
    def getType(self):
        if (self.type is self.TK_IDENTIFIER):
            tokenType = 'Identificador'
        if (self.type is self.TK_SPECIAL_CHAR):
            tokenType = 'Caractere Especial'
        if (self.type is self.TK_RESERVED_WORD):
            tokenType = 'Palavra Reservada'
        elif (self.type is self.TK_INT):
            tokenType = 'Inteiro'
        elif (self.type is self.TK_FLOAT):
            tokenType = 'Float'
        elif (self.type is self.TK_ARITHMETIC_OPERATOR):
            tokenType = 'Operador Aritmético'
        elif (self.type is self.TK_RELATIONAL_OPERATOR):
            tokenType = 'Operador Relacional'
        elif (self.type is self.TK_CHAR):
            tokenType = 'Char'
        return tokenType

    def __repr__(self):
        return 'Token [Tipo: ' + self.getType() + ' | Texto: ' + self.text + ' | Linha: ' + str(self.line) + ' | Coluna: ' + str(self.column) + ']'
