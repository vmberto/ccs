import utils as u
from token_model import Token

global pos
global line
global column
pos = 0
column = 1
line = 1

try:
    txtContent = open('txt', 'r').read()
    content = list(txtContent)
except Exception as e:
    print(e)


def nextToken():
    if (isEOF()):
        return None
    global column, line

    term = ''
    state = 0
    token = None
    while (token == None):
        currentChar = nextChar()
        column += 1

        if (state is 0):
            if (not u.isChar(currentChar) and u.isSpecialChar(currentChar)):
                term += currentChar
                return Token(Token.TK_SPECIAL_CHAR, term, line, column)
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
                line += 1
                column = 0

        elif (state is 1):
            if (u.isChar(currentChar) or u.isDigit(currentChar)):
                term += currentChar
                state = 1

            elif (term.count('\'') == 2 and term[0] == '\'' and term[2] == '\''):
                return Token(Token.TK_CHAR if u.isChar(term[1]) else Token.TK_DIGIT, term, line, column)
            
            elif (term.count('\'') == 0 and (u.isSpace(currentChar) or u.isOperator(currentChar) or u.isEOF(currentChar) or u.isSpecialChar(currentChar))):
                if (not u.isEOF(currentChar)):
                    back()

                if (u.isReservedWord(term)):
                    return Token(Token.TK_RESERVED_WORD, term, line, column)
                else:
                    return Token(Token.TK_IDENTIFIER, term, line, column)
            else:
                term += currentChar
                raise Exception('Malformed Identifier: ' + term)

        elif (state is 2):
            if (u.isDigit(currentChar) or currentChar is '.'):
                term += currentChar
                state = 2

            elif ((not u.isChar(currentChar) or u.isEOF(currentChar)) and u.isFloatOrInt(term)):
                if (not u.isEOF(currentChar)):
                    back()
                if (term.count('.') is 1):
                    return Token(Token.TK_FLOAT, term, line, column)
                else:
                    return Token(Token.TK_INT, term, line, column)
            else:
                term += currentChar
                raise Exception('Unrecognized NUMBER: ' + term)

        elif (state is 3):
            if (u.isOperator(currentChar)):
                term += currentChar
                state = 3
            elif (u.isChar(currentChar) or u.isDigit(currentChar) or u.isSpace(currentChar) or u.isEOF(currentChar)):
                if (not u.isEOF(currentChar)):
                    back()
                if (u.isArithmeticOperator(term)):
                    return Token(Token.TK_ARITHMETIC_OPERATOR, term, line, column)
                elif(u.isRelationalOperator(term)):
                    return Token(Token.TK_RELATIONAL_OPERATOR, term, line, column)
                else:
                    term += currentChar
                    raise Exception('Unrecognized OPERATOR: ' + term)
            else:
                term += currentChar
                raise Exception('Unrecognized OPERATOR: ' + term)
    return None


def back():
    global pos, column
    column -= 1
    pos -= 1


def nextChar():
    if (isEOF()):
        return '\0'
    global pos
    char = content[pos]
    pos += 1
    return char


def isEOF():
    return pos == len(content)


def main():
    while True:
        try:
            token = nextToken()
            if (token == None):
                break
            else:
                print(token)
        except Exception as e:
            print(e)


if (__name__ == '__main__'):
    main()

# falta por os EOFs
