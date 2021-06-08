import sys
from lexical.lexical_analysis import LexicalAnalysis 
from syntax.syntax_analysis import SyntaxAnalysis 

def main():
    (code_name, code_content) = readCode()
    al = LexicalAnalysis(code_name, code_content)
    sa = SyntaxAnalysis(al)
    
    print('\n-------- Syntax --------')
    try:
        sa.execute()
        print('Successfully Parsed')
    except Exception as e:
        print(e)


def readCode():
    code = ''
    code_name = 'code.c'
    try:
        code_name = sys.argv[1]
        code = open(code_name, "r").read()
    except Exception as e:
        code = open(code_name, "r").read()
    return [code_name, list(code)]
    
if (__name__ == '__main__'):
    main()