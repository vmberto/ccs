import utils as u
from token_model import Token

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
        BlockScopeParser(self.box).execute(mainExecution = True)

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

    def execute(self, mainExecution = False):
        self.expectOpeningCurlyBracket()
        while(not self.expectClosingCurlyBracket()):
            self.box['token'] = self.box['scanner'].nextToken()
            attp = AttributionParser(self.box)
            cep = ConditionalExpressionParser(self.box)
            lp = LoopParser(self.box)
            # o cep precisa ficar acima, pois a verificação por ELSE no final avança um token
            if (cep.checkTokenCompatibility()):
                cep.execute()
            if (lp.checkTokenCompatibility()):
                lp.execute()
            if (attp.checkTokenCompatibility()):
                attp.execute()
            if (self.box['token'].type != Token.TK_SPECIAL_CHAR):
                raise Exception('syntax error: unexpected token, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

        self.box['token'] = self.box['scanner'].nextToken()
        if (not mainExecution and not self.box['token']):
            raise Exception('syntax error: unexpected end of file!')

    def expectOpeningCurlyBracket(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != '{'):
            raise Exception('opening curly braces Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def expectClosingCurlyBracket(self):
        return self.box['token'].text is '}'

class ArithmeticParser:

    def __init__(self, box, typeDeclaration = None):
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
            raise Exception('int value Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))
        if (self.box['token'].type != Token.TK_IDENTIFIER and self.box['token'].type != Token.TK_INT and self.box['token'].type != Token.TK_FLOAT and self.box['token'].type != Token.TK_CHAR):
            raise Exception('identifier or number Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))
    
    def expectArithmeticOperator(self):
        if (self.box['token'].type != Token.TK_ARITHMETIC_OPERATOR):
            raise Exception('operator Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def expectSemicolon(self):
        return (self.box['token'].text == ';')

    def checkTokenCompatibility(self):
        return self.box['token'].type is Token.TK_IDENTIFIER or self.box['token'].type is Token.TK_INT or self.box['token'].type is Token.TK_FLOAT or self.box['token'].type is Token.TK_ARITHMETIC_OPERATOR

class AttributionParser:

    def __init__(self, box):
        self.box = box
        self.typeDeclaration = None

    def execute(self, reexecution = False):
        if (not reexecution):
            self.expectVariableTypeDeclaration()
        self.expectIdentifier()
        self.expectAttributionOperator()

        ap = ArithmeticParser(self.box, self.typeDeclaration)
        ap.execute()

        self.expectSemicolonOrComma()

        if (self.box['token'].text == ','):
            self.execute(reexecution = True)

    def expectVariableTypeDeclaration(self):
        if (not self.checkTokenCompatibility()):
            raise Exception('type Declaration Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))
        else:
            self.typeDeclaration = self.box['token'].text 

    def expectIdentifier(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].type != Token.TK_IDENTIFIER):
            raise Exception('identifier Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def expectAttributionOperator(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != '='):
            raise Exception('attribution operator Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def expectIntValue(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].type != Token.TK_INT):
            raise Exception('int value Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))
    
    def expectFloatValue(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].type != Token.TK_FLOAT and self.box['token'].type != Token.TK_INT):
            raise Exception('float value Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def expectCharValue(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].type != Token.TK_CHAR):
            raise Exception('char value Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def expectSemicolonOrComma(self):
        if (self.box['token'].text != ';' and self.box['token'].text != ','):
            raise Exception('semicolon or comma Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def checkTokenCompatibility(self):
        return self.box['token'].type is Token.TK_RESERVED_WORD and (self.box['token'].text == 'int' or self.box['token'].text == 'float' or self.box['token'].text == 'char')

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
            raise Exception('relational operator Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

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
            raise Exception('if Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def elseExists(self):
        return self.box['token'].text == 'else'
            
    def expectOpeningParenthesis(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != '('):
            raise Exception('opening Parenthesis Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def expectClosingParenthesis(self):
        if (self.box['token'].text != ')'):
            raise Exception('closing Parenthesis Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

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
            raise Exception('if Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def expectOpeningParenthesis(self):
        self.box['token'] = self.box['scanner'].nextToken()
        if (self.box['token'].text != '('):
            raise Exception('opening Parenthesis Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def expectClosingParenthesis(self):
        if (self.box['token'].text != ')'):
            raise Exception('closing Parenthesis Expected!, found ' + self.box['token'].getType() + ' ( ' + self.box['token'].text + ' ) at LINE ' + str(self.box['token'].line) + ' and COLUMN ' + str(self.box['token'].column))

    def checkTokenCompatibility(self):
        return self.box['token'].type is Token.TK_RESERVED_WORD and self.box['token'].text == 'while'
