import re

def isDigit(char):
    pattern = r"^[0-9.]{1}$"
    return bool(re.match(pattern, char))

def isChar(char):
    pattern = r"^[a-zA-Z_']{1}$"
    return bool(re.match(pattern, char))

def isOperator(char):
    return isRelationalOperator(char) or isArithmeticOperator(char) or isConditionalOperator(char)

def isExclamationMark(char):
    return char == '!'

def isRelationalOperator(char):
    return char in ['<', '>', '<=', '>=', '==', '!=']

def isConditionalOperator(char):
    return char in ['&', '&&', '|', '||']

def isArithmeticOperator(char):
    return char in ['+', '-', '*', '/', '=', '++', '--']

def isAssignmentOperator(char):
    return char == '='

def isSpecialChar(char):
    return char in ['(', ')', '[', ']', ',', ';', '{', '}']

def isSpace(char):
    return char.isspace()

def isEOF(char):
    return char is '\0'

def isFloatOrInt(term):
    return bool(re.match(r"^[+-]?(\d+((\.|\,)\d*)?|(\.|\,)\d+)([eE][+-]?\d+)?$", term)) and term[0] != '.' and term[len(term)-1] != '.'

def isReservedWord(term):
    return term in ['main', 'if', 'else', 'while', 'do', 'for', 'int', 'float', 'char']

def countLine(char):
    return char is '\n' or char is '\r'
