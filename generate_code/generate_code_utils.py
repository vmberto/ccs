def invert(exp):
    if (exp.find('<=') > -1):
        exp = exp.replace('<=', '>')
    elif (exp.find('>=') > -1):
        exp = exp.replace('>=', '<')
    elif (exp.find('==') > -1):
        exp = exp.replace('==', '!=')
    elif (exp.find('<') > -1):
        exp = exp.replace('<', '>=')
    elif (exp.find('>') > -1):
        exp = exp.replace('>', '<=')
    return exp