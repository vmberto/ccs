from semantic.semantic_exception import SemanticException

class SemanticAnalysis:

    def __init__(self):
        self.symbolTable = []

    def insertSymbol(self, newSymbol, isDeclaring):

        if (newSymbol.value):
            newSymbol.setValue(eval(newSymbol.value))
        
        if (newSymbol.type == 'int' and newSymbol.value and newSymbol.value % 1 != 0):
            raise SemanticException('Variable (' + newSymbol.identifier + ') of type int with floating point value (' + str(newSymbol.value) + ')')

        if (not isDeclaring):
            symbol = self.checkIdentifierExistence(newSymbol.identifier, newSymbol.scope, identifierValueInUse=False)
            if (symbol.type == 'int' and newSymbol.value and newSymbol.value % 1 != 0):
                raise SemanticException('Variable (' + newSymbol.identifier + ') of type int with floating point value (' + str(newSymbol.value) + ')')
            symbol.value = newSymbol.value
        else:
            for symbol in self.symbolTable:
                if (
                    symbol.identifier == newSymbol.identifier and
                    symbol.scope == newSymbol.scope and isDeclaring
                ):
                    raise SemanticException('Variable (' + str(newSymbol.identifier) + ') already declared')
            self.symbolTable.append(newSymbol)


    def checkIdentifierExistence(self, identifier, scope, identifierValueInUse = True):
        for symbol in self.symbolTable:
            if (
                symbol.identifier == identifier and
                symbol.scope <= scope
            ):
                if (identifierValueInUse and not symbol.value):
                    raise SemanticException("Variable (" + symbol.identifier + ') was declared but not initialized')

                return symbol
        
        raise SemanticException("Variable (" + str(identifier) + ") undeclared")

    def outputSymbolTable(self, code_name): #pragma: no cover
        text_file = open(__file__.replace('/semantic/semantic_analysis.py', '') + "/output/" + code_name + "_symbol_table", "w")
        for symbol in self.symbolTable:
            text_file.write(symbol.__repr__() + '\n')
        text_file.close()
                

