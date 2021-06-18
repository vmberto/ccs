import ccs2.syntax.syntax_utils as u
from ccs2.syntax.syntax_exception import SyntaxException
from ccs2.lexical.token_model import Token
from ccs2.syntax.syntax_exception import SyntaxException

def expectNextToBeClosingParenthesis(self):
    self.box['token'] = self.box['scanner'].getNextToken()
    if (self.box['token'] is None or self.box['token'].text != ')'):
        raise SyntaxException('closing Parenthesis Expected')

def expectNextToBeIntDeclaration(s):
    s.box['token'] = s.box['scanner'].getNextToken()
    if (s.box['token'] is None or s.box['token'].text != 'int'):
        raise SyntaxException('type declaration for main identifier Expected', s.box['token'])

def expectNextToBeMainDeclaration(s):
    s.box['token'] = s.box['scanner'].getNextToken()
    if (s.box['token'] is None or s.box['token'].text != 'main'):
        raise SyntaxException('main identifier Expected', s.box['token'])

def expectNextToBeOperningCurlyBracket(s):
    s.box['token'] = s.box['scanner'].getNextToken()
    if (s.box['token'].text != '{'):
        raise SyntaxException('opening curly braces Expected', s.box['token'])

def expectNumberOrIdentifier(s):
    if (s.box['token'].type != Token.TK_IDENTIFIER and s.box['token'].type != Token.TK_INT and s.box['token'].type != Token.TK_FLOAT and s.box['token'].type != Token.TK_CHAR):
        raise SyntaxException('identifier or number Expected', s.box['token'])

def expectArithmeticOperator(s):
    if (s.box['token'].type != Token.TK_ARITHMETIC_OPERATOR):
        raise SyntaxException('operator Expected', s.box['token'])

def expectNextAttrOperatorOrSemicolonOrComma(s):
    s.box['token'] = s.box['scanner'].getNextToken()
    if (not u.isAttributionOperator(s.box['token'].text) and not u.isComma(s.box['token'].text) and not u.isSemicolon(s.box['token'].text)):
        raise SyntaxException('attribution operator, semicolon or comma Expected', s.box['token'])

def expectSemicolonOrComma(s):
    if (not u.isComma(s.box['token'].text) and not u.isSemicolon(s.box['token'].text)):
        raise SyntaxException('semicolon or comma Expected', s.box['token'])

def expectRelationalOperator(s):
    if (s.box['token'].type != Token.TK_RELATIONAL_OPERATOR):
        raise SyntaxException('relational operator Expected', s.box['token'])

def expectNextToBeOpeningParenthesis(s):
    s.box['token'] = s.box['scanner'].getNextToken()
    if (s.box['token'] is None or s.box['token'].text != '('):
        raise SyntaxException('opening Parenthesis Expected', s.box['token'])

def expectClosingParenthesis(s):
    if (s.box['token'].text != ')'):
        raise SyntaxException('closing Parenthesis Expected', s.box['token'])

def expectIdentifier(self):
    if (self.box['token'].type != Token.TK_IDENTIFIER):
        raise SyntaxException('identifier Expected', self.box['token'])