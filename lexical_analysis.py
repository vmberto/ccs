import utils as u
from token_model import Token

class LexicalAnalysis:

    def __init__(self):
        self.line = 1
        self.pos = 0
        self.column = 0
        try:
            txtContent = open('code.c', 'r').read()
            self.content = list(txtContent)
        except Exception as e:
            print(e)
            self.content = ''

    
    def nextToken(self):
        if (self.isEOF()):
            return None

        term = ''
        state = 0
        token = None
        while (token == None):
            currentChar = self.nextChar()
            self.column += 1

            if (state is 0):
                if (not u.isChar(currentChar) and u.isSpecialChar(currentChar)):
                    term += currentChar
                    return Token(Token.TK_SPECIAL_CHAR, term, self.line, self.column)
                elif (u.isChar(currentChar)):
                    term += currentChar
                    state = 1
                elif (u.isDigit(currentChar)):
                    state = 2
                    term += currentChar
                elif (u.isOperator(currentChar)):
                    term += currentChar
                    state = 3
                elif (u.isSpace(currentChar)):
                    state = 0
                elif (u.isEOF(currentChar)):
                    break
                else:
                    raise Exception('Unrecognized SYMBOL: ' + term)

                if (u.countLine(currentChar)):
                    self.line += 1
                    self.column = 0

            elif (state is 1):
                if (u.isChar(currentChar) or u.isDigit(currentChar)):
                    term += currentChar
                    state = 1

                elif (term.count('\'') == 2 and term[0] == '\'' and term[2] == '\''):
                    return Token(Token.TK_CHAR if u.isChar(term[1]) else Token.TK_DIGIT, term, self.line, self.column)
                
                elif (term.count('\'') == 0 and (u.isSpace(currentChar) or u.isOperator(currentChar) or u.isEOF(currentChar) or u.isSpecialChar(currentChar))):
                    if (not u.isEOF(currentChar)):
                        self.back()

                    if (u.isReservedWord(term)):
                        return Token(Token.TK_RESERVED_WORD, term, self.line, self.column)
                    else:
                        return Token(Token.TK_IDENTIFIER, term, self.line, self.column)
                else:
                    term += currentChar
                    raise Exception('Malformed Identifier: ' + term)

            elif (state is 2):
                if (u.isDigit(currentChar) or u.isChar(currentChar) or currentChar is '.'):
                    term += currentChar
                    state = 2

                elif ((not u.isChar(currentChar) or u.isEOF(currentChar)) and u.isFloatOrInt(term)):
                    if (not u.isEOF(currentChar)):
                        self.back()
                    if (term.count('.') is 1):
                        return Token(Token.TK_FLOAT, term, self.line, self.column)
                    else:
                        return Token(Token.TK_INT, term, self.line, self.column)
                else:
                    term += currentChar
                    raise Exception('Unrecognized NUMBER: ' + term)

            elif (state is 3):
                if (u.isOperator(currentChar)):
                    term += currentChar
                    state = 3
                elif (u.isChar(currentChar) or u.isDigit(currentChar) or u.isSpace(currentChar) or u.isEOF(currentChar)):
                    if (not u.isEOF(currentChar)):
                        self.back()
                    if (u.isArithmeticOperator(term)):
                        return Token(Token.TK_ARITHMETIC_OPERATOR, term, self.line, self.column)
                    elif(u.isRelationalOperator(term)):
                        return Token(Token.TK_RELATIONAL_OPERATOR, term, self.line, self.column)
                    else:
                        term += currentChar
                        raise Exception('Unrecognized OPERATOR: ' + term)
                else:
                    term += currentChar
                    raise Exception('Unrecognized OPERATOR: ' + term)
        return None

    def back(self):
        self.column -= 1
        self.pos -= 1


    def nextChar(self):
        if (self.isEOF()):
            return '\0'
        char = self.content[self.pos]
        self.pos += 1
        return char


    def isEOF(self):
        return self.pos == len(self.content)
