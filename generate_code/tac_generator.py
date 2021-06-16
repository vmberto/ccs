import ast
import re

def evalAll(x):
    return eval(x)


class GetTACSequence:

    def __init__(self, expression):
        self.vars = {}
        self.ops = []
        self.evaluate(ast.parse(expression, mode='eval').body)

        for val in self.ops:
            self.vars['t' + str(len(self.vars))] = val

        allValues = {}
        for val in self.vars:
            if (not any(c.isalpha() for c in str(self.vars[val]))):
                allValues[val] = str(eval(str(self.vars[val])))

        for val in self.vars:
            if isinstance(self.vars[val], str):
                if ('+' in self.vars[val]):
                    x,y = self.vars[val].split('+')
                elif ('-' in self.vars[val]):
                    x,y = self.vars[val].split('-')
                elif ('*' in self.vars[val]):
                    x,y = self.vars[val].split('*')
                else:
                    x,y = self.vars[val].split('/')
                res = dict((v,k) for k,v in allValues.items())

                if (x in list(allValues.values())):
                    self.vars[val] = re.sub(rf'\b{x}\b', res[x], self.vars[val])
                if (y in list(allValues.values())):
                    self.vars[val] = re.sub(rf'\b{y}\b', res[y], self.vars[val])

    def evaluate(self, theoperation): 

        if (isinstance(theoperation, ast.Name)):
            return theoperation.id

        if (isinstance(theoperation, ast.Num)):
            if (not theoperation.n in self.vars.values()):
                self.vars['t' + str(len(self.vars))] = theoperation.n
            
            return theoperation.n
                
        if (isinstance(theoperation, ast.BinOp)):
            left = self.evaluate(theoperation.left)
            right = self.evaluate(theoperation.right)
            hasIdentifier = False

            if isinstance(left, str) or isinstance(right, str):
                hasIdentifier = True
            
            if (isinstance(theoperation.op, ast.Add)):
                if (not (str(left) + '+' + str(right)) in self.vars.values()):
                    self.vars['t' + str(len(self.vars))] = (str(left) + '+' + str(right))
                return left + right if not hasIdentifier else 't' + str(len(self.vars) - 1)
            elif (isinstance(theoperation.op, ast.Sub)):
                if (not (str(left) + '-' + str(right)) in self.vars.values()):
                    self.vars['t' + str(len(self.vars))] = (str(left) + '-' + str(right))
                return left + right if not hasIdentifier else 't' + str(len(self.vars) - 1)
            elif (isinstance(theoperation.op, ast.Mult)):
                if (not (str(left) + '*' + str(right)) in self.vars.values()):
                    self.vars['t' + str(len(self.vars))] = (str(left) + '*' + str(right))
                return left + right if not hasIdentifier else 't' + str(len(self.vars) - 1)
            elif (isinstance(theoperation.op, ast.Div)):
                if (not (str(left) + '/' + str(right)) in self.vars.values()):
                    self.vars['t' + str(len(self.vars))] = (str(left) + '/' + str(right))
                return left + right if not hasIdentifier else 't' + str(len(self.vars) - 1)
            
    def getSequence(self):
        return self.vars
