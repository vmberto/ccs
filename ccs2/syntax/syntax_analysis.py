from ccs2.generate_code.generate_code import GenerateCode
from ccs2.semantic.symbol import Symbol
from ccs2.lexical.token_model import Token
from ccs2.syntax.syntax_exception import SyntaxException
import ccs2.syntax.syntax_utils as u
from ccs2.syntax.syntax_expects import *

class SyntaxAnalysis:

    def __init__(self, scanner, semantic):
        self.box = {
            "scanner": scanner,
            "token": None,
            "scope": 0,
            "semantic": semantic,
        }

    def execute(self):
        expectNextToBeIntDeclaration(self)
        expectNextToBeMainDeclaration(self)
        expectNextToBeOpeningParenthesis(self)
        expectNextToBeClosingParenthesis(self)
        BlockScopeParser(self.box).execute(mainExecution=True)

class BlockScopeParser:

    def __init__(self, box):
        self.box = box
        self.attp = AttributionParser(self.box)
        self.cep = ConditionalExpressionParser(self.box)
        self.lp = LoopParser(self.box)

    def execute(self, mainExecution=False):
        expectNextToBeOperningCurlyBracket(self)
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
            self.execute()
            expectClosingParenthesis(self)
            self.expression = self.expression + ')'
        else:
            expectNumberOrIdentifier(self)
            if (self.box['token'].type == Token.TK_IDENTIFIER):
                self.expression = self.expression + str(self.box['semantic'].checkIdentifierExistence(self.box['token'].text, self.box['scope']).identifier)
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
                self.execute()
                expectClosingParenthesis(self)
                self.expression = self.expression + ')'
            else:
                expectNumberOrIdentifier(self)
                if (self.box['token'].type == Token.TK_IDENTIFIER):
                    identifierValue = str(self.box['semantic'].checkIdentifierExistence(self.box['token'].text, self.box['scope']).identifier)
                    self.expression = self.expression + identifierValue
                else:
                    self.expression = self.expression + self.box['token'].text

            self.executeL()

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

        if (self.isDeclaring):
            newSymbol.setType(self.box['token'].text)

        if (type):
            newSymbol.setType(type)

        if (self.isDeclaring or (reexecution and not self.isDeclaring)):
            self.box['token'] = self.box['scanner'].getNextToken()

        expectIdentifier(self)

        newSymbol.setIdentifier(self.box['token'].text)

        expectNextAttrOperatorOrSemicolonOrComma(self)

        if (u.isAttributionOperator(self.box['token'].text)):
            expression = self.ap.executeAndGetResult()
            newSymbol.setInitialized(True)
            self.box['semantic'].insertSymbol(newSymbol, expression, self.isDeclaring)
            expectSemicolonOrComma(self)
            self.checkCommaAndExecute(newSymbol.type)
            GenerateCode().writeAttribution(newSymbol, expression)
        else:
            self.box['semantic'].insertSymbol(newSymbol, isDeclaring=self.isDeclaring)
            self.checkCommaAndExecute(newSymbol.type)
        

    def checkCommaAndExecute(self, type):
        if (u.isComma(self.box['token'].text)):
            self.execute(type=type, reexecution=True)

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
        expressionA = self.ap.executeAndGetResult()
        expectRelationalOperator(self)
        operator = self.box['token'].text
        expressionB = self.ap.executeAndGetResult()

        if (self.box['token'].type == Token.TK_CONDITIONAL_OPERATOR):
            self.execute()

        return expressionA, operator, expressionB

class ConditionalExpressionParser:

    def __init__(self, box):
        self.box = box

    def execute(self):
        expectNextToBeOpeningParenthesis(self)
        expressionA, operator, expressionB = ConditionalOperationParser(self.box).execute()
        expectClosingParenthesis(self)

        GenerateCode().writeIf(expressionA, operator, expressionB)

        BlockScopeParser(self.box).execute()
        
        if (self.checkIfElseExists()):
            GenerateCode().writeGoto()
            GenerateCode().writeLabel()
            BlockScopeParser(self.box).execute()
            GenerateCode().writeLabel()
        else:
            GenerateCode().writeLabel()


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

        expectNextToBeOpeningParenthesis(self)

        expressionA, operator, expressionB = ConditionalOperationParser(self.box).execute()

        expectClosingParenthesis(self)

        GenerateCode().writeLabel(loop=True)

        BlockScopeParser(self.box).execute()

        GenerateCode().writeLoop(expressionA, operator, expressionB)


    def isLoopStatement(self):
        return self.box['token'].text == 'while'
