from semantic.symbol_variable import SymbolVariable
from semantic.symbol_conditional_statement import SymbolConditionalStatement
import lexical.lexical_utils as u
import sys
import os
from lexical.token_model import Token
from lexical.lexical_exception import LexicalException

class GenerateCode:

    def __init__(self, code_name, symbolTable):
        self.text_file = open(__file__.replace('/generate_code/generate_code.py', '') + "/output/" + code_name + "_intermediary", "w")
        self.labelLine = False
        self.labelNumber = 0
        
        for symbol in symbolTable:
            if (isinstance(symbol, SymbolVariable)):
                var = str(symbol.identifier) + str(symbol.scope)
                self.writeLine(var + ' = ' + var + ' + ' + str(symbol.value))
            if (isinstance(symbol, SymbolConditionalStatement) and symbol.type == 'if'):
                self.generateConditional(symbol)
            if (isinstance(symbol, SymbolConditionalStatement) and symbol.type == 'ifend'):
                self.writeLabel()
            if (isinstance(symbol, SymbolConditionalStatement) and symbol.type == 'else'):
                self.generateConditional(symbol)
            if (isinstance(symbol, SymbolConditionalStatement) and symbol.type == 'elseend'):
                self.writeLabel()

            if (isinstance(symbol, SymbolConditionalStatement) and symbol.type == 'while'):
                if (not self.labelLine):
                    self.writeLabel()
            if (isinstance(symbol, SymbolConditionalStatement) and symbol.type == 'whileend'):
                self.generateLoop(symbol)
        self.text_file.close()

    def generateConditional(self, symbol):
        self.labelNumber += 1
        self.writeLine('if (' + self.invert(symbol.expression) + ') goto L' + str(self.labelNumber))

    def generateLoop(self, symbol):
        self.writeLine('if (' + self.invert(symbol.expression) + ') goto L' + str(self.labelNumber))

    def invert(self, exp):
        if (exp.find('<') > -1):
            exp = exp.replace('<', '>=')

        elif (exp.find('>') > -1):
            exp = exp.replace('>', '<=')

        elif (exp.find('<=') > -1):
            exp = exp.replace('<=', '>')

        elif (exp.find('>=') > -1):
            exp = exp.replace('>=', '<')

        elif (exp.find('==') > -1):
            exp = exp.replace('==', '!=')

        return exp

    def writeLabel(self):
        self.text_file.write('L'+ str(self.labelNumber) + ': ')
        self.labelLine = True

    def writeLine(self, str):
        if (self.labelLine):
            self.text_file.write(str + '\n')
            self.labelLine = False
        else:  
            self.text_file.write('    ' + str + '\n')

