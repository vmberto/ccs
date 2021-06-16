class Symbol:

    def __init__(self, scope):
        self.type = ''
        self.identifier = ''
        self.value = ''
        self.scope = scope
    
    def setType(self, type):
        self.type = type

    def setValue(self, value):
        self.value = value

    def setScope(self, scope):
        self.scope = scope

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return 'SymbolVariable [Type: ' + self.type + ' | Identificador: ' + self.identifier + ' | Value: ' + str(self.value) + ' | Escopo: ' + str(self.scope) + ']'