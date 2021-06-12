class SymbolConditionalStatement:

    def __init__(self, type, expression = ''):
        self.type = type
        self.expression = expression
        self.identifier = ''
    
    def __repr__(self):
        return 'SymbolConditionalStatement [Type: ' + self.type + ' | Value: ' + str(self.expression) + ']'