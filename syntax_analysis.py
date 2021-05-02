import utils as u
from token_model import Token
from syntax_exception import SyntaxException


class Parser:

    def __init__(self, scanner):
        self.box = {
            "scanner": scanner,
            "token": None
        }

    def execute(self):
        self.expectIntDeclaration()
        self.expectMainDeclaration()
        self.expectOpeningParenthesis()
        self.expectClosingParenthesis()
        BlockScopeParser(self.box).execute(mainExecution=True)

    def expectIntDeclaration(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != 'int'):
            raise Exception('int Expected!')

    def expectMainDeclaration(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != 'main'):
            raise Exception('main Expected!')

    def expectOpeningParenthesis(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != '('):
            raise Exception('openingParenthesis Expected!')

    def expectClosingParenthesis(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != ')'):
            raise Exception('closingParenthesis Expected!')


class BlockScopeParser:

    def __init__(self, box):
        self.box = box

    def execute(self, mainExecution=False):
        self.expectOpeningCurlyBracket()
        while(not self.expectClosingCurlyBracket()):
            self.box['token'] = self.box['scanner'].nextToken()
            attp = AttributionParser(self.box)
            decp = DeclarationParser(self.box)
            cep = ConditionalExpressionParser(self.box)
            lp = LoopParser(self.box)
            if (lp.checkTokenCompatibility()):
                lp.execute()
            if (attp.checkTokenCompatibility()):
                attp.execute()
            if (cep.checkTokenCompatibility()):
                cep.execute()
            if (decp.checkTokenCompatibility()):
                decp.execute()
            if (self.box['token'].type != Token.TK_SPECIAL_CHAR):
                raise SyntaxException('unexpected token', self.box['token'])

        self.box['token'] = self.box['scanner'].nextToken()
        if (not mainExecution and not self.box['token']):
            raise SyntaxException('unexpected end of file', self.box['token'])

    def expectOpeningCurlyBracket(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != '{'):
            raise SyntaxException(
                'opening curly braces Expected', self.box['token'])

    def expectClosingCurlyBracket(self):
        return self.box['token'].text is '}'


class ArithmeticParser:

    def __init__(self, box, typeDeclaration=None):
        self.box = box
        self.typeDeclaration = typeDeclaration

    def execute(self):
        self.expectNumberOrIdentifier()
        self.executeL()

    def executeL(self):
        token = self.box['token']
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'] != None and (self.checkTokenCompatibility())):
            self.expectArithmeticOperator()
            token = self.box['token']
            self.expectNumberOrIdentifier()
            self.executeL()

    def expectNumberOrIdentifier(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.typeDeclaration == 'int' and self.box['token'].type == Token.TK_FLOAT):
            raise SyntaxException('int value Expected', self.box['token'])
        if (self.box['token'].type != Token.TK_IDENTIFIER and self.box['token'].type != Token.TK_INT and self.box['token'].type != Token.TK_FLOAT and self.box['token'].type != Token.TK_CHAR):
            raise SyntaxException(
                'identifier or number Expected', self.box['token'])

    def expectArithmeticOperator(self):
        if (self.box['token'].type != Token.TK_ARITHMETIC_OPERATOR):
            raise SyntaxException('operator Expected', self.box['token'])

    def checkTokenCompatibility(self):
        return self.box['token'].type is Token.TK_IDENTIFIER or self.box['token'].type is Token.TK_INT or self.box['token'].type is Token.TK_FLOAT or (self.box['token'].type is Token.TK_ARITHMETIC_OPERATOR and self.box['token'].text != '=')


class DeclarationParser:

    def __init__(self, box):
        self.box = box
        self.typeDeclaration = None

    def execute(self, reexecution=False):
        if (not reexecution):
            self.expectVariableTypeDeclaration()
        self.expectIdentifier()
        self.expectNextAttrOperatorOrSemicolonOrComma()
        if (self.isAttributionOperator()):
            ap = ArithmeticParser(self.box, self.typeDeclaration)
            ap.execute()
        elif (self.isComma()):
            self.execute(reexecution=True)

    def expectVariableTypeDeclaration(self):
        if (not self.checkTokenCompatibility()):
            raise SyntaxException(
                'type Declaration Expected', self.box['token'])
        else:
            self.typeDeclaration = self.box['token'].text

    def expectIdentifier(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].type != Token.TK_IDENTIFIER):
            raise SyntaxException('identifier Expected', self.box['token'])

    def expectNextAttrOperatorOrSemicolonOrComma(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (not self.isAttributionOperator() and not self.isComma() and not self.isSemicolon()):
            raise SyntaxException('attribution operator Expected', self.box['token'])

    def expectCurrentAttrOperatorOrSemicolonOrComma(self):
        if (not self.isAttributionOperator() and not self.isComma() and not self.isSemicolon()):
            raise SyntaxException('attribution operator, semicolon or comma Expected', self.box['token'])
    
    def isComma(self):
        return self.box['token'].text == ','

    def isSemicolon(self):
        return self.box['token'].text == ';'

    def isAttributionOperator(self):
        return self.box['token'].text == '='

    def checkTokenCompatibility(self):
        return (self.box['token'].text == 'int' or self.box['token'].text == 'float' or self.box['token'].text == 'char')


class AttributionParser(DeclarationParser):

    def __init__(self, box):
        self.box = box

    def execute(self, reexecution=False):
        if (reexecution):
            self.expectIdentifier()
        self.expectNextAttrOperatorOrSemicolonOrComma()
        ap = ArithmeticParser(self.box)
        ap.execute()
        self.expectCurrentAttrOperatorOrSemicolonOrComma()
        if (self.isComma()):
            self.execute(reexecution = True)

    def checkTokenCompatibility(self):
        return self.box['token'].type is Token.TK_IDENTIFIER


class ConditionalOperationParser:

    def __init__(self, box):
        self.box = box

    def execute(self):
        ap = ArithmeticParser(self.box)
        ap.execute()
        self.expectRelationalOperator()
        ap.execute()

    def expectRelationalOperator(self):
        if (self.box['token'].type != Token.TK_RELATIONAL_OPERATOR):
            raise SyntaxException('relational operator Expected', self.box['token'])

    def expectSemicolon(self):
        return (self.box['token'].text == ';')

class ConditionalExpressionParser:

    def __init__(self, box):
        self.box = box

    def execute(self, reexecution = False):
        self.expectIf()
        self.expectOpeningParenthesis()

        cop = ConditionalOperationParser(self.box)
        cop.execute()

        self.expectClosingParenthesis()

        BlockScopeParser(self.box).execute()

        if (self.elseExists()):
            BlockScopeParser(self.box).execute()

    def expectIf(self):
        if (not self.checkTokenCompatibility()):
            raise SyntaxException('if Expected', self.box['token'])

    def elseExists(self):
        return self.box['token'].text == 'else'
            
    def expectOpeningParenthesis(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != '('):
            raise SyntaxException('opening Parenthesis Expected', self.box['token'])

    def expectClosingParenthesis(self):
        if (self.box['token'].text != ')'):
            raise SyntaxException('closing Parenthesis Expected', self.box['token'])

    def checkTokenCompatibility(self):
        return self.box['token'].type is Token.TK_RESERVED_WORD and self.box['token'].text == 'if'

class LoopParser:

    def __init__(self, box):
        self.box = box

    def execute(self, reexecution = False):
        self.expectWhile()
        self.expectOpeningParenthesis()

        cop = ConditionalOperationParser(self.box)
        cop.execute()

        self.expectClosingParenthesis()

        BlockScopeParser(self.box).execute()

    def expectWhile(self):
        if (not self.checkTokenCompatibility()):
            raise SyntaxException('if Expected', self.box['token'])

    def expectOpeningParenthesis(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != '('):
            raise SyntaxException('opening Parenthesis Expected', self.box['token'])

    def expectClosingParenthesis(self):
        if (self.box['token'].text != ')'):
            raise SyntaxException('closing Parenthesis Expected', self.box['token'])

    def checkTokenCompatibility(self):
        return self.box['token'].type is Token.TK_RESERVED_WORD and self.box['token'].text == 'while'
