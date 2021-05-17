import utils as u
import sys
import os
from lexical.token_model import Token
from lexical.lexical_exception import LexicalException

class LexicalAnalysis:

    def __init__(self, code_name, code_content, output = True):
        if not os.path.exists('output'):
            os.makedirs('output')
        self.line = 1
        self.column = 0
        self.position = 0
        self.code_content = code_content
        self.tokens = []
        if (output):
            text_file = open("output/" + code_name + "_lex_tokens" , "w")
        while True:
            try:
                token = self.saveNextToken()
                
                if (token == None):
                    self.position = 0
                    break
                else:
                    if (output):
                        text_file.write(token.__repr__() + '\n')
                    self.tokens.append(token)
            except Exception as e:
                text_file.write(e.__str__() + '\n')
        if (output):
            text_file.close()

    def saveNextToken(self):
        if (self.isEOF()):
            return None

        term = ''
        state = 0
        while (True):
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
                elif (u.isOperator(currentChar) or u.isExclamationMark(currentChar)):
                    term += currentChar
                    state = 3
                elif (u.isSpace(currentChar)):
                    state = 0
                elif (u.isEOF(currentChar)):
                    break
                else:
                    raise LexicalException('unrecognized SYMBOL [ ' + currentChar + ' ]')

                if (u.countLine(currentChar)):
                    self.line += 1
                    self.column = 0

            elif (state is 1):
                if (u.isChar(currentChar) or u.isDigit(currentChar) and currentChar != ';'):
                    term += currentChar
                    state = 1

                elif (term.count('\'') == 2 and term[0] == '\'' and term[2] == '\''):
                    if (not u.isEOF(currentChar)):
                        self.back()
                    return Token(Token.TK_CHAR, term, self.line, self.column)
                
                elif (term.count('\'') == 0 and (u.isSpace(currentChar) or u.isOperator(currentChar) or u.isEOF(currentChar) or u.isSpecialChar(currentChar))):
                    if (not u.isEOF(currentChar)):
                        self.back()

                    if (u.isReservedWord(term)):
                        return Token(Token.TK_RESERVED_WORD, term, self.line, self.column)
                    else:
                        return Token(Token.TK_IDENTIFIER, term, self.line, self.column)
                else:
                    term += currentChar
                    raise LexicalException('Malformed Identifier [ ' + term + ' ] ')

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
                    raise LexicalException('unrecognized NUMBER [ ' + term + ' ] ')

            elif (state is 3):
                if (u.isOperator(currentChar)):
                    term += currentChar
                    state = 3
                elif (u.isOperator(currentChar) or u.isChar(currentChar) or u.isDigit(currentChar) or u.isSpace(currentChar) or u.isEOF(currentChar) or currentChar == ';'):
                    if (not u.isEOF(currentChar)):
                        self.back()
                    if (u.isAssignmentOperator(term)):
                        return Token(Token.TK_ASSIGNMENT_OPERATOR, term, self.line, self.column)
                    elif (u.isConditionalOperator(term)):
                        return Token(Token.TK_CONDITIONAL_OPERATOR, term, self.line, self.column)
                    elif (u.isArithmeticOperator(term)):
                        return Token(Token.TK_ARITHMETIC_OPERATOR, term, self.line, self.column)
                    elif(u.isRelationalOperator(term)):
                        return Token(Token.TK_RELATIONAL_OPERATOR, term, self.line, self.column)
                    else:
                        raise LexicalException('unrecognized OPERATOR [ ' + term + ' ] ')
                else:
                    term += currentChar
                    raise LexicalException('unrecognized OPERATOR [ ' + term + ' ] ')
        return None

    def back(self):
        self.column -= 1
        self.position -= 1

    def nextChar(self):
        if (self.isEOF()):
            return '\0'
        char = self.code_content[self.position]
        self.position += 1
        return char

    def isEOF(self):
        return self.position == len(self.code_content)

    def getTokens(self):
        return self.tokens

    def getNextToken(self):
        if (len(self.tokens) == self.position):
            return None
        token = self.tokens[self.position]
        self.position += 1
        return token

    def getPreviousToken(self):
        self.position -= 2
        token = self.tokens[self.position]
        self.position += 1
        return token
