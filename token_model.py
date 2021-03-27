class Token:
    TK_IDENTIFIER     = 0
    TK_SPECIAL_CHAR   = 1
    TK_RESERVED_WORD  = 2
    TK_INT            = 3
    TK_FLOAT          = 4
    TK_ARITHMETIC_OPERATOR = 5
    TK_RELATIONAL_OPERATOR = 6
    TK_CHAR = 7
    TK_DIGIT = 8

    def __init__(self, tokenType, text, line, column):
        self.type = tokenType
        self.text = text
        self.line = line
        self.column = column

    def __repr__(self):
        if (self.type is 0):
            tokenType = 'Identificador'
        if (self.type is 1):
            tokenType = 'Caractere Especial'
        if (self.type is 2):
            tokenType = 'Palavra Reservada'
        elif (self.type is 3):
            tokenType = 'Inteiro'
        elif (self.type is 4):
            tokenType = 'Float'
        elif (self.type is 5):
            tokenType = 'Operador Aritmético'
        elif (self.type is 6):
            tokenType = 'Operador Relacional'
        elif (self.type is 7):
            tokenType = 'Char'
        elif (self.type is 8):
            tokenType = 'Dígito' 
        return 'Token [Tipo: ' + tokenType + ' | Texto: ' + self.text + ' | Linha: ' + str(self.line) + ' | Coluna: ' + str(self.column) + ']'
