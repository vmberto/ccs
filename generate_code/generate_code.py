from utils.singleton import Singleton
from generate_code.tac_generator import GetTACSequence
import lexical.lexical_utils as u
import sys
import os

class GenerateCode(metaclass=Singleton):

    def __init__(self):
        self.labelLine = False
        self.labelNumber = 0
        self.labels = []
        self.lines = []
                
    def writeAttribution(self, symbol, expression):
        result = self.writeArithmeticExpression(expression)
        self.saveLine(symbol.identifier + ' = ' + result)

    def writeIf(self, expressionA, operator, expressionB):

        resultA = self.writeArithmeticExpression(expressionA)
        resultB = self.writeArithmeticExpression(expressionB)

        self.labelNumber += 1
        self.saveLine('if (' + resultA + ' ' + self.invert(operator) + ' ' + resultB + ') goto L' + str(self.labelNumber))
        self.labels.insert(0, 'L' + str(self.labelNumber))

    def writeGoto(self):
        self.labelNumber += 1
        self.saveLine('goto L' + str(self.labelNumber))
        self.labels.insert(1, 'L' + str(self.labelNumber))

    def writeLabel(self, loop = False):
        self.labelLine = True
        if (loop):
            self.labelNumber += 1
            self.saveLine('L' + str(self.labelNumber) + ':', is_label=True)
            self.labels.insert(1, 'L' + str(self.labelNumber))
        elif (len(self.labels) <= 0):
            self.labelNumber += 1
            self.saveLine('L' + str(self.labelNumber) + ':', is_label=True)
        else:
            self.saveLine(self.labels.pop(0) + ':', is_label=True)

    def writeLoop(self, expressionA, operator, expressionB):
        resultA = self.writeArithmeticExpression(expressionA)
        resultB = self.writeArithmeticExpression(expressionB)
        self.saveLine('if (' + resultA + ' ' + operator + ' ' + resultB + ') goto L' + str(self.labelNumber))
        
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

    def saveLine(self, str, is_label=False):
        if (self.labelLine and is_label):
            self.lines.append('\n' + str)
        elif (self.labelLine):
            self.lines.append(' ' + str + '\n')
            self.labelLine = False
        else:
            self.lines.append('    ' + str + '\n')

    def writeArithmeticExpression(self, expression):
        expressionDict = GetTACSequence(expression).getSequence()

        if (len(expressionDict.values()) > 1):
            resultA = str(list(expressionDict.keys())[-1])
            for key in expressionDict:
                    if (isinstance(expressionDict[key], str)):
                        self.saveLine(key + ' = ' + expressionDict[key])
                    else:
                        self.saveLine(key + ' = ' + str(expressionDict[key]))
        else:
            resultA = expression

        return resultA
        
    def saveCode(self, code_name):
        self.text_file = open(__file__.replace('/generate_code/generate_code.py', '') + "/output/" + code_name + "_intermediary", "w")
        self.text_file.writelines(self.lines)
        self.text_file.close()