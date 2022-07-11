class Symbol: # pragma: no coverage

    def __init__(self, scope):
        self.type = ''
        self.identifier = ''
        self.initialized = False
        self.scope = scope
    
    def setType(self, type):
        self.type = type

    def setInitialized(self, initialized):
        self.initialized = initialized

    def setScope(self, scope):
        self.scope = scope

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return 'Symbol [Type: ' + self.type + ' | Identifier: ' + self.identifier + ' | Initialized: ' + str(self.initialized) + ' | Scope: ' + str(self.scope) + ']'