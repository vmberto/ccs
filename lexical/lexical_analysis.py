import lexical.lexical_utils as u
import sys
import os
from lexical.token_model import Token
from lexical.lexical_exception import LexicalException

class LexicalAnalysis:

    def __init__(self, code_content):
        if not os.path.exists('output'): # pragma: no cover
            os.makedirs('output')
        self.__line = 1
        self.__column = 0
        self.__position = 0
        self.__code_content = code_content
        self.tokens = []
        self.errors = []
        while True:
            try:
                token = self.__saveNextToken()
                
                if (token == None):
                    self.__position = 0
                    break
                else:
                    self.tokens.append(token)
            except Exception as e:
                self.tokens.append(e)
                self.errors.append(e)

    def __saveNextToken(self):
        if (self.__isEOF()):
            return None

        term = ''
        state = 0
        while (True):
            currentChar = self.__nextChar()
            self.__column += 1

            if (state is 0):
                if (not u.isChar(currentChar) and u.isSpecialChar(currentChar)):
                    term += currentChar
                    return Token(Token.TK_SPECIAL_CHAR, term, self.__line, self.__column)
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
                    self.__line += 1
                    self.__column = 0

            elif (state is 1):
                if (u.isChar(currentChar) or u.isDigit(currentChar) and currentChar != ';'):
                    term += currentChar
                    state = 1

                elif (term.count('\'') == 2 and term[0] == '\'' and term[2] == '\''):
                    if (not u.isEOF(currentChar)):
                        self.__back()
                    return Token(Token.TK_CHAR, term, self.__line, self.__column)
                
                elif (term.count('\'') == 0 and (u.isSpace(currentChar) or u.isOperator(currentChar) or u.isEOF(currentChar) or u.isSpecialChar(currentChar))):
                    if (not u.isEOF(currentChar)):
                        self.__back()

                    if (u.isReservedWord(term)):
                        return Token(Token.TK_RESERVED_WORD, term, self.__line, self.__column)
                    else:
                        return Token(Token.TK_IDENTIFIER, term, self.__line, self.__column)
                else:
                    term += currentChar
                    raise LexicalException('Malformed Identifier [ ' + term + ' ] ')

            elif (state is 2):
                if (u.isDigit(currentChar) or u.isChar(currentChar) or currentChar is '.'):
                    term += currentChar
                    state = 2
                elif ((not u.isChar(currentChar) or u.isEOF(currentChar)) and u.isFloatOrInt(term)):
                    if (not u.isEOF(currentChar)):
                        self.__back()
                    if (term.count('.') is 1):
                        return Token(Token.TK_FLOAT, term, self.__line, self.__column)
                    else:
                        return Token(Token.TK_INT, term, self.__line, self.__column)
                else:
                    term += currentChar
                    raise LexicalException('unrecognized NUMBER [ ' + term + ' ] ')

            elif (state is 3):
                if (u.isOperator(currentChar)):
                    term += currentChar
                    state = 3
                elif (u.isOperator(currentChar) or u.isChar(currentChar) or u.isDigit(currentChar) or u.isSpace(currentChar) or u.isEOF(currentChar) or currentChar == ';'):
                    if (not u.isEOF(currentChar)):
                        self.__back()
                    if (u.isAssignmentOperator(term)):
                        return Token(Token.TK_ASSIGNMENT_OPERATOR, term, self.__line, self.__column)
                    elif (u.isConditionalOperator(term)):
                        return Token(Token.TK_CONDITIONAL_OPERATOR, term, self.__line, self.__column)
                    elif (u.isArithmeticOperator(term)):
                        return Token(Token.TK_ARITHMETIC_OPERATOR, term, self.__line, self.__column)
                    elif(u.isRelationalOperator(term)):
                        return Token(Token.TK_RELATIONAL_OPERATOR, term, self.__line, self.__column)
                    else:
                        raise LexicalException('unrecognized OPERATOR [ ' + term + ' ] ')
                else:
                    term += currentChar
                    raise LexicalException('unrecognized OPERATOR [ ' + term + ' ] ')
        return None

    def __back(self):
        self.__column -= 1
        self.__position -= 1

    def __nextChar(self):
        if (self.__isEOF()):
            return '\0'
        char = self.__code_content[self.__position]
        self.__position += 1
        return char

    def __isEOF(self):
        return self.__position == len(self.__code_content)

    def getNextToken(self):
        if (len(self.tokens) == self.__position):
            return None
        token = self.tokens[self.__position]
        self.__position += 1
        return token

    def getPreviousToken(self):
        self.__position -= 2
        token = self.tokens[self.__position]
        self.__position += 1
        return token

    def outputLexicalTokens(self, code_name): #pragma: no cover
        text_file = open(__file__.replace('/lexical/lexical_analysis.py', '') + "/output/" + code_name + "_lex_tokens", "w")
        for token in self.tokens:
            text_file.write(token.__repr__() + '\n')
        text_file.close()
