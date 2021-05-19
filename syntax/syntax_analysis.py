import utils as u
from lexical.token_model import Token
from syntax.syntax_exception import SyntaxException

class SyntaxAnalysis:

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
        while(not self.expectClosingCurlyBracket()):
            if (self.attp.checkTokenCompatibility()):
                self.attp.execute()
            elif (self.lp.checkTokenCompatibility()):
                self.lp.execute()
            elif (self.cep.checkTokenCompatibility()):
                self.cep.execute()
            elif (self.box['token'].type != Token.TK_SPECIAL_CHAR):
                raise SyntaxException('unexpected token', self.box['token'])
            self.box['token'] = self.box['scanner'].getNextToken()

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
        self.analyzingAutoIncrementOperation = False
        self.asubexpp = ArithmeticSubExpressionParser(self.box)

    def execute(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.asubexpp.checkTokenCompatibility()):
            self.asubexpp.execute()
        else:
            if (self.checkIfAutoOperator()):
                self.box['token'] = self.box['scanner'].getNextToken()
                self.expectIdentifier()
                self.analyzingAutoIncrementOperation = True
            else:
                self.expectNumberOrIdentifier()
        self.executeL()

    def executeL(self):
        previousToken = self.box['token']
        self.box['token'] = self.box['scanner'].getNextToken()

        if (self.checkIfAutoOperator()):
            self.validateIfCurrentAutoOperation()
            self.expectIdentifier(previousToken)
            self.box['token'] = self.box['scanner'].getNextToken()

        if (self.box['token'] != None and (self.checkTokenCompatibility())):
            self.expectArithmeticOperator() 
            self.analyzingAutoIncrementOperation = False
            self.box['token'] = self.box['scanner'].getNextToken()
            if (self.asubexpp.checkTokenCompatibility()):
                self.asubexpp.execute()
            else:
                if (self.checkIfAutoOperator()):
                    self.box['token'] = self.box['scanner'].getNextToken()
                    self.expectIdentifier()
                    self.analyzingAutoIncrementOperation = True
                else:
                    self.expectNumberOrIdentifier()
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

    def checkIfAutoOperator(self):
        return (self.box['token'].text == '++' or self.box['token'].text == '--')

    def checkTokenCompatibility(self):
        return self.box['token'].type is Token.TK_IDENTIFIER or self.box['token'].type is Token.TK_INT or self.box['token'].type is Token.TK_FLOAT or (self.box['token'].type is Token.TK_ARITHMETIC_OPERATOR and self.box['token'].text != '=' and self.box['token'].text != ';')

class ArithmeticSubExpressionParser:
    def __init__(self, box):
        self.box = box

    def execute(self, reexecution = False):
        self.expectOpeningParenthesis()

        ap = ArithmeticParser(self.box)
        ap.execute()
        
        self.expectClosingParenthesis()

    def expectOpeningParenthesis(self):
        if (self.box['token'].text != '('):
            raise SyntaxException('opening Parenthesis Expected', self.box['token'])

    def expectClosingParenthesis(self):
        if (self.box['token'].text != ')'):
            raise SyntaxException('closing Parenthesis Expected', self.box['token'])

    def checkTokenCompatibility(self):
        return self.box['token'].text == '('

class AttributionParser:

    def __init__(self, box):
        self.box = box
        self.isDeclaring = True
        self.ap = ArithmeticParser(self.box)

    def execute(self, reexecution=False):
        if (not reexecution and self.isDeclaring):
            self.expectVariableTypeDeclaration()
        self.expectIdentifier(reexecution)
        self.expectNextAttrOperatorOrSemicolonOrComma()
        if (self.isAttributionOperator()):
            self.ap.execute()
            self.expectSemicolonOrComma()
            self.checkCommaAndExecute()
        else:
            self.checkCommaAndExecute()

    def checkCommaAndExecute(self):
        if (self.isComma()):
            self.execute(reexecution=True)

    def expectVariableTypeDeclaration(self):
        if (not self.checkTokenCompatibility()):
            raise SyntaxException(
                'type Declaration Expected', self.box['token'])

    def expectIdentifier(self, reexecution):
        if (self.isDeclaring or (reexecution and not self.isDeclaring)):
            self.box['token'] = self.box['scanner'].getNextToken()
        if (self.box['token'].type != Token.TK_IDENTIFIER):
            raise SyntaxException('identifier Expected', self.box['token'])

    def expectNextAttrOperatorOrSemicolonOrComma(self):
        self.box['token'] = self.box['scanner'].getNextToken()
        if (not self.isAttributionOperator() and not self.isComma() and not self.isSemicolon()):
            raise SyntaxException('attribution operator, semicolon or comma Expected', self.box['token'])

    def expectSemicolonOrComma(self):
        if (not self.isComma() and not self.isSemicolon()):
            raise SyntaxException('semicolon or comma Expected', self.box['token'])

    def isComma(self):
        return self.box['token'].text == ','

    def isSemicolon(self):
        return self.box['token'].text == ';'

    def isAttributionOperator(self):
        return self.box['token'].text == '='

    def checkTokenCompatibility(self):
        if (self.box['token'].type == Token.TK_IDENTIFIER):
            self.isDeclaring = False
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
        self.expectIf()
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

    def expectIf(self):
        if (not self.checkTokenCompatibility()):
            raise SyntaxException('if Expected', self.box['token'])

    def elseExists(self):
        return self.box['token'].text == 'else'
            
    def expectOpeningParenthesis(self):
        self.box['token'] = self.box['scanner'].getNextToken()
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

    def execute(self):
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
        self.box['token'] = self.box['scanner'].getNextToken()
        if (self.box['token'].text != '('):
            raise SyntaxException('opening Parenthesis Expected', self.box['token'])

    def expectClosingParenthesis(self):
        if (self.box['token'].text != ')'):
            raise SyntaxException('closing Parenthesis Expected', self.box['token'])

    def checkTokenCompatibility(self):
        return self.box['token'].type is Token.TK_RESERVED_WORD and self.box['token'].text == 'while'
