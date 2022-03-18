from ccs2.generate_code.generate_code import GenerateCode
import sys
import datetime
from ccs2.utils.logger import log
from ccs2.lexical.lexical_analysis import LexicalAnalysis 
from ccs2.syntax.syntax_analysis import SyntaxAnalysis 
from ccs2.semantic.semantic_analysis import SemanticAnalysis
import os

class Compile:

    def __init__(self, code_name = '', code_content = '', testing = False):
        begin_time = datetime.datetime.now()
        
        if (not code_content): #pragma: no coverage
            try:
                (code_name, code_content) = self.readCode()
            except Exception:
                log('Nenhum código encontrado', 'error', testing)
                return

        log('Compiling...', 'waiting', testing)

        la = LexicalAnalysis(code_content)
        sema = SemanticAnalysis()
        syna = SyntaxAnalysis(la, sema)

        try:
            syna.execute()
            execution_time = datetime.datetime.now() - begin_time
            log('Successfully Compiled in ' + str(execution_time), 'success', testing)
        except Exception as e:
            if (testing):
                raise e
            else: #pragma: no coverage
                log(e, 'error', testing)

        if (not testing): #pragma: no coverage
            MYDIR = ('output')
            CHECK_FOLDER = os.path.isdir(MYDIR)
            if not CHECK_FOLDER:
                os.makedirs(MYDIR)
            sema.outputSymbolTable(code_name)
            la.outputLexicalTokens(code_name)
            GenerateCode().saveCode(code_name)

    def readCode(self): #pragma: no coverage
        code = ''
        code_name = 'code.c'
        try:
            code_name = sys.argv[1]
            code = open(code_name, "r").read()
        except Exception as e:
            code = open(code_name, "r").read()
        return [code_name, list(code)]

def main(): #pragma: no coverage
    Compile()
    
if (__name__ == '__main__'): #pragma: no coverage
    main()