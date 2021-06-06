import syntax.syntax_utils as u
from syntax.syntax_exception import SyntaxException
from lexical.token_model import Token
from syntax.syntax_exception import SyntaxException

def expectIntDeclaration(self):
    self.box['token'] = self.box['scanner'].getNextToken()
    if (self.box['token'].text != 'int'):
        raise SyntaxException('type declaration for main identifier Expected', self.box['token'])

def expectMainDeclaration(self):
    self.box['token'] = self.box['scanner'].getNextToken()
    if (self.box['token'].text != 'main'):
        raise SyntaxException('main identifier Expected', self.box['token'])

def expectOpeningParenthesis(self):
    self.box['token'] = self.box['scanner'].getNextToken()
    if (self.box['token'].text != '('):
        raise SyntaxException('opening parentheesis Expected!')

def expectClosingParenthesis(self):
    self.box['token'] = self.box['scanner'].getNextToken()
    if (self.box['token'].text != ')'):
        raise SyntaxException('closing parenthesis Expected!')

def expectOpeningCurlyBracket(self):
    self.box['token'] = self.box['scanner'].getNextToken()
    if (self.box['token'].text != '{'):
        raise SyntaxException(
            'opening curly braces Expected', self.box['token'])

def expectNumberOrIdentifier(self):
    if (self.box['token'].type != Token.TK_IDENTIFIER and self.box['token'].type != Token.TK_INT and self.box['token'].type != Token.TK_FLOAT and self.box['token'].type != Token.TK_CHAR):
        raise SyntaxException('identifier or number Expected', self.box['token'])

def expectIdentifier(self, token = None):
    if (token.type != Token.TK_IDENTIFIER if token else self.box['token'].type != Token.TK_IDENTIFIER):
        raise SyntaxException('identifier for auto-operator Expected', token if token else self.box['token'])

def expectArithmeticOperator(self):
    if (self.box['token'].type != Token.TK_ARITHMETIC_OPERATOR):
        raise SyntaxException('operator Expected', self.box['token'])

def expectOpeningParenthesis(self):
    if (self.box['token'].text != '('):
        raise SyntaxException('opening Parenthesis Expected', self.box['token'])

def expectClosingParenthesis(self):
    if (self.box['token'].text != ')'):
        raise SyntaxException('closing Parenthesis Expected', self.box['token'])

def expectVariableTypeDeclaration(self):
    if (not self.isAttributionStatement()):
        raise SyntaxException(
            'type Declaration Expected', self.box['token'])

def expectIdentifier(self, reexecution):
    if (self.isDeclaring or (reexecution and not self.isDeclaring)):
        self.box['token'] = self.box['scanner'].getNextToken()
    if (self.box['token'].type != Token.TK_IDENTIFIER):
        raise SyntaxException('identifier Expected', self.box['token'])

def expectNextAttrOperatorOrSemicolonOrComma(self):
    self.box['token'] = self.box['scanner'].getNextToken()
    if (not u.isAttributionOperator(self.box['token'].text) and not u.isComma(self.box['token'].text) and not u.isSemicolon(self.box['token'].text)):
        raise SyntaxException('attribution operator, semicolon or comma Expected', self.box['token'])

def expectSemicolonOrComma(self):
    if (not u.isComma(self.box['token'].text) and not u.isSemicolon(self.box['token'].text)):
        raise SyntaxException('semicolon or comma Expected', self.box['token'])

def expectRelationalOperator(self):
    if (self.box['token'].type != Token.TK_RELATIONAL_OPERATOR):
        raise SyntaxException('relational operator Expected', self.box['token'])

def expectOpeningParenthesis(self):
    self.box['token'] = self.box['scanner'].getNextToken()
    if (self.box['token'].text != '('):
        raise SyntaxException('opening Parenthesis Expected', self.box['token'])

def expectClosingParenthesis(self):
    if (self.box['token'].text != ')'):
        raise SyntaxException('closing Parenthesis Expected', self.box['token'])

def expectOpeningParenthesis(self):
    self.box['token'] = self.box['scanner'].getNextToken()
    if (self.box['token'].text != '('):
        raise SyntaxException('opening Parenthesis Expected', self.box['token'])

def expectClosingParenthesis(self):
    if (self.box['token'].text != ')'):
        raise SyntaxException('closing Parenthesis Expected', self.box['token'])