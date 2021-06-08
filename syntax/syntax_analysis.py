from semantic.semantic_analysis import SemanticAnalysis
from semantic.symbol import Symbol
from lexical.token_model import Token
from syntax.syntax_exception import SyntaxException
import syntax.syntax_utils as u

class SyntaxAnalysis:

    def __init__(self, scanner):
        self.box = {
            "scanner": scanner,
            "token": None,
            "scope": 0,
            "semantic": SemanticAnalysis()
        }

    def execute(self):
        self.expectIntDeclaration()
        self.expectMainDeclaration()
        self.expectOpeningParenthesis()
        self.expectClosingParenthesis()
        BlockScopeParser(self.box).execute(mainExecution=True)

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

class BlockScopeParser:

    def __init__(self, box):
        self.box = box
        self.attp = AttributionParser(self.box)
        self.cep = ConditionalExpressionParser(self.box)
        self.lp = LoopParser(self.box)

    def execute(self, mainExecution=False):
        self.expectOpeningCurlyBracket()
        self.box['scope'] += 1
        while(not self.expectClosingCurlyBracket()):
            if (self.attp.isAttributionStatement()):
                self.attp.execute()
            elif (self.lp.isLoopStatement()):
                self.lp.execute()
            elif (self.cep.isConditionalStatement()):
                self.cep.execute()
            elif (self.box['token'].type != Token.TK_SPECIAL_CHAR):
                raise SyntaxException('unexpected token', self.box['token'])
            self.box['token'] = self.box['scanner'].getNextToken()

        self.box['scope'] -= 1
        self.box['token'] = self.box['scanner'].getNextToken()
        if (not mainExecution and not self.box['token']):
            raise SyntaxException('unexpected end of file')
        self.box['token'] = self.box['scanner'].getPreviousToken()

    def expectOpeningCurlyBracket(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.box['token'].text != '{'):
            raise SyntaxException(
                'opening curly braces Expected', self.box['token'])

    def expectClosingCurlyBracket(self):
        if (self.box['token'] is None):
            raise SyntaxException('unexpected end of file')
        return self.box['token'].text is '}'

class ArithmeticParser:

    def __init__(self, box):
        self.box = box
        self.completeExpression = ''

    def executeAndGetResult(self):
        self.execute()
        result = self.completeExpression
        self.completeExpression = ''
        return result

    def execute(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.isOpeningSubexpression()):
            self.completeExpression = self.completeExpression + '('
            self.expectOpeningParenthesis()
            self.execute()
            self.expectClosingParenthesis()
            self.completeExpression = self.completeExpression + ')'
        else:
            self.expectNumberOrIdentifier()
            if (self.box['token'].type == Token.TK_IDENTIFIER):
                self.completeExpression = self.completeExpression + str(self.box['semantic'].checkIdentifierExistence(self.box['token'].text, self.box['scope']).value)
            else:
                self.completeExpression = self.completeExpression + self.box['token'].text 
        self.executeL()


    def executeL(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.box['token'] != None and (self.checkTokenCompatibility())):
            self.expectArithmeticOperator()
            self.completeExpression = self.completeExpression + self.box['token'].text
            self.box['token'] = self.box['scanner'].getNextToken()
            if (self.isOpeningSubexpression()):
                self.completeExpression = self.completeExpression + ' ( '
                self.expectOpeningParenthesis()
                self.execute()
                self.expectClosingParenthesis()
                self.completeExpression = self.completeExpression + ' ) '
            else:
                self.expectNumberOrIdentifier()
                if (self.box['token'].type == Token.TK_IDENTIFIER):
                    identifierValue = str(self.box['semantic'].checkIdentifierExistence(self.box['token'].text, self.box['scope']).value)
                    self.completeExpression = self.completeExpression + identifierValue
                else:
                    self.completeExpression = self.completeExpression + self.box['token'].text

            self.executeL()

    def expectNumberOrIdentifier(self):
        if (self.box['token'].type != Token.TK_IDENTIFIER and self.box['token'].type != Token.TK_INT and self.box['token'].type != Token.TK_FLOAT and self.box['token'].type != Token.TK_CHAR):
            raise SyntaxException('identifier or number Expected', self.box['token'])
        
    def expectIdentifier(self, token = None):
        if (token.type != Token.TK_IDENTIFIER if token else self.box['token'].type != Token.TK_IDENTIFIER):
            raise SyntaxException('identifier for auto-operator Expected', token if token else self.box['token'])

    def expectArithmeticOperator(self):
        if (self.box['token'].type != Token.TK_ARITHMETIC_OPERATOR):
            raise SyntaxException('operator Expected', self.box['token'])

    def validateIfCurrentAutoOperation(self):
        if (self.analyzingAutoIncrementOperation):
            raise SyntaxException('invalid operation with dual auto-operators', self.box['token'])   

    def expectOpeningParenthesis(self):
        if (self.box['token'].text != '('):
            raise SyntaxException('opening Parenthesis Expected', self.box['token'])

    def expectClosingParenthesis(self):
        if (self.box['token'].text != ')'):
            raise SyntaxException('closing Parenthesis Expected', self.box['token'])

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
            self.expectVariableTypeDeclaration()
            newSymbol.setType(self.box['token'].text)

        if (type):
            newSymbol.setType(type)

        self.expectIdentifier(reexecution)
        newSymbol.setIdentifier(self.box['token'].text)

        self.expectNextAttrOperatorOrSemicolonOrComma()

        if (u.isAttributionOperator(self.box['token'].text)):
            expression = self.ap.executeAndGetResult()
            newSymbol.setValue(expression)
            self.box['semantic'].insertSymbol(newSymbol, self.isDeclaring)
            self.expectSemicolonOrComma()
            self.checkCommaAndExecute(newSymbol.type)
        else:
            newSymbol.setValue(None)
            self.box['semantic'].insertSymbol(newSymbol, self.isDeclaring)
            self.checkCommaAndExecute(newSymbol.type)

    def checkCommaAndExecute(self, type):
        if (u.isComma(self.box['token'].text)):
            self.execute(type=type, reexecution=True)

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
        self.expectRelationalOperator()
        self.ap.execute()

        if (self.box['token'].type == Token.TK_CONDITIONAL_OPERATOR):
            self.execute()

    def expectRelationalOperator(self):
        if (self.box['token'].type != Token.TK_RELATIONAL_OPERATOR):
            raise SyntaxException('relational operator Expected', self.box['token'])

    def expectSemicolon(self):
        return (self.box['token'].text == ';')

class ConditionalExpressionParser:

    def __init__(self, box):
        self.box = box

    def execute(self):
        self.expectOpeningParenthesis()

        cop = ConditionalOperationParser(self.box)
        cop.execute()

        self.expectClosingParenthesis()

        BlockScopeParser(self.box).execute()
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.elseExists()):
            BlockScopeParser(self.box).execute()
        else:
            self.box['token'] = self.box['scanner'].getPreviousToken()

    def elseExists(self):
        return self.box['token'].text == 'else'
            
    def expectOpeningParenthesis(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.box['token'].text != '('):
            raise SyntaxException('opening Parenthesis Expected', self.box['token'])

    def expectClosingParenthesis(self):
        if (self.box['token'].text != ')'):
            raise SyntaxException('closing Parenthesis Expected', self.box['token'])

    def isConditionalStatement(self):
        return Token.TK_RESERVED_WORD and self.box['token'].text == 'if'

class LoopParser:

    def __init__(self, box):
        self.box = box

    def execute(self):
        self.expectOpeningParenthesis()

        cop = ConditionalOperationParser(self.box)
        cop.execute()

        self.expectClosingParenthesis()

        BlockScopeParser(self.box).execute()

    def expectOpeningParenthesis(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.box['token'].text != '('):
            raise SyntaxException('opening Parenthesis Expected', self.box['token'])

    def expectClosingParenthesis(self):
        if (self.box['token'].text != ')'):
            raise SyntaxException('closing Parenthesis Expected', self.box['token'])

    def isLoopStatement(self):
        return Token.TK_RESERVED_WORD and self.box['token'].text == 'while'
