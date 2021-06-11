from semantic.semantic_analysis import SemanticAnalysis
from semantic.symbol import Symbol
from lexical.token_model import Token
from syntax.syntax_exception import SyntaxException
import syntax.syntax_utils as u
from syntax.syntax_expects import *

class SyntaxAnalysis:

    def __init__(self, scanner, semantic):
        self.box = {
            "scanner": scanner,
            "token": None,
            "scope": 0,
            "semantic": semantic
        }

    def execute(self):
        expectIntDeclaration(self)
        expectMainDeclaration(self)
        expectOpeningParenthesis(self)
        self.expectClosingParenthesis()
        BlockScopeParser(self.box).execute(mainExecution=True)

    def expectClosingParenthesis(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.box['token'].text != ')'):
            raise SyntaxException('closing parenthesis Expected!')

class BlockScopeParser:

    def __init__(self, box):
        self.box = box
        self.attp = AttributionParser(self.box)
        self.cep = ConditionalExpressionParser(self.box)
        self.lp = LoopParser(self.box)

    def execute(self, mainExecution=False):
        expectOpeningCurlyBracket(self)
        self.enterNewScope()

        while(not self.waitForClosingCurlyBracket()):

            if (self.attp.isAttributionStatement()):
                self.attp.execute()
            elif (self.lp.isLoopStatement()):
                self.lp.execute()
            elif (self.cep.isConditionalStatement()):
                self.cep.execute()
            elif (self.box['token'].type != Token.TK_SPECIAL_CHAR):
                raise SyntaxException('unexpected token', self.box['token'])

            self.box['token'] = self.box['scanner'].getNextToken()

        self.leaveScope()

        self.box['token'] = self.box['scanner'].getNextToken()
        if (not mainExecution and not self.box['token']):
            raise SyntaxException('unexpected end of file')
        self.box['token'] = self.box['scanner'].getPreviousToken()

    def waitForClosingCurlyBracket(self):
        if (self.box['token'] is None):
            raise SyntaxException('unexpected end of file')
        return self.box['token'].text is '}'

    def enterNewScope(self):
        self.box['scope'] += 1

    def leaveScope(self):
        self.box['scope'] -= 1
    
class ArithmeticParser:

    def __init__(self, box):
        self.box = box
        self.expression = ''

    def executeAndGetResult(self):
        self.execute()
        result = self.expression
        self.expression = ''
        return result

    def execute(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.isOpeningSubexpression()):
            self.expression = self.expression + '('
            self.expectOpeningParenthesis()
            self.execute()
            expectClosingParenthesis(self)
            self.expression = self.expression + ')'
        else:
            expectNumberOrIdentifier(self)
            if (self.box['token'].type == Token.TK_IDENTIFIER):
                self.expression = self.expression + str(self.box['semantic'].checkIdentifierExistence(self.box['token'].text, self.box['scope']).value)
            else:
                self.expression = self.expression + self.box['token'].text 
        self.executeL()


    def executeL(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.box['token'] != None and (self.checkTokenCompatibility())):
            expectArithmeticOperator(self)
            self.expression = self.expression + self.box['token'].text
            self.box['token'] = self.box['scanner'].getNextToken()
            if (self.isOpeningSubexpression()):
                self.expression = self.expression + '('
                self.expectOpeningParenthesis()
                self.execute()
                expectClosingParenthesis(self)
                self.expression = self.expression + ')'
            else:
                expectNumberOrIdentifier(self)
                if (self.box['token'].type == Token.TK_IDENTIFIER):
                    identifierValue = str(self.box['semantic'].checkIdentifierExistence(self.box['token'].text, self.box['scope']).value)
                    self.expression = self.expression + identifierValue
                else:
                    self.expression = self.expression + self.box['token'].text

            self.executeL()

    def expectOpeningParenthesis(self):
        if (self.box['token'].text != '('):
            raise SyntaxException('opening Parenthesis Expected', self.box['token'])

    def isOpeningSubexpression(self):
        return self.box['token'].text == '('

    def checkTokenCompatibility(self):
        return self.box['token'].type is Token.TK_IDENTIFIER or self.box['token'].type is Token.TK_INT or self.box['token'].type is Token.TK_FLOAT or (self.box['token'].type is Token.TK_ARITHMETIC_OPERATOR and self.box['token'].text != '=' and self.box['token'].text != ';')

class AttributionParser:

    def __init__(self, box):
        self.box = box
        self.isDeclaring = True
        self.ap = ArithmeticParser(self.box)

    def execute(self, reexecution=False, type=None):
        newSymbol = Symbol(self.box['scope'])

        if (not reexecution and self.isDeclaring):
            expectVariableTypeDeclaration(self)
            newSymbol.setType(self.box['token'].text)

        if (type):
            newSymbol.setType(type)

        self.expectIdentifier(reexecution)

        newSymbol.setIdentifier(self.box['token'].text)

        expectNextAttrOperatorOrSemicolonOrComma(self)

        if (u.isAttributionOperator(self.box['token'].text)):
            expression = self.ap.executeAndGetResult()
            newSymbol.setValue(expression)
            self.box['semantic'].insertSymbol(newSymbol, self.isDeclaring)
            expectSemicolonOrComma(self)
            self.checkCommaAndExecute(newSymbol.type)
        else:
            newSymbol.setValue(None)
            self.box['semantic'].insertSymbol(newSymbol, self.isDeclaring)
            self.checkCommaAndExecute(newSymbol.type)

    def checkCommaAndExecute(self, type):
        if (u.isComma(self.box['token'].text)):
            self.execute(type=type, reexecution=True)

    def expectIdentifier(self, reexecution):
        if (self.isDeclaring or (reexecution and not self.isDeclaring)):
            self.box['token'] = self.box['scanner'].getNextToken()
        if (self.box['token'].type != Token.TK_IDENTIFIER):
            raise SyntaxException('identifier Expected', self.box['token'])

    def isAttributionStatement(self):
        if (self.box['token'].type == Token.TK_IDENTIFIER):
            self.isDeclaring = False
        else:
            self.isDeclaring = True
        return (self.box['token'].text == 'int' 
            or self.box['token'].text == 'float' 
            or self.box['token'].text == 'char' 
            or self.box['token'].type == Token.TK_IDENTIFIER)

class ConditionalOperationParser:

    def __init__(self, box):
        self.box = box
        self.ap = ArithmeticParser(self.box)

    def execute(self):
        self.ap.execute()
        expectRelationalOperator(self)
        self.ap.execute()

        if (self.box['token'].type == Token.TK_CONDITIONAL_OPERATOR):
            self.execute()

class ConditionalExpressionParser:

    def __init__(self, box):
        self.box = box

    def execute(self):
        expectOpeningParenthesis(self)

        ConditionalOperationParser(self.box).execute()

        expectClosingParenthesis(self)

        BlockScopeParser(self.box).execute()

        if (self.checkIfElseExists()):
            BlockScopeParser(self.box).execute()

    def checkIfElseExists(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        elseExists = self.box['token'].text == 'else'
        if (not elseExists):
            self.box['token'] = self.box['scanner'].getPreviousToken()
        return elseExists
            
    def isConditionalStatement(self):
        return self.box['token'].text == 'if'

class LoopParser:

    def __init__(self, box):
        self.box = box

    def execute(self):

        expectOpeningParenthesis(self)

        ConditionalOperationParser(self.box).execute()

        expectClosingParenthesis(self)

        BlockScopeParser(self.box).execute()

    def isLoopStatement(self):
        return self.box['token'].text == 'while'
