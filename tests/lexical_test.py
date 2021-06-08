from syntax.syntax_analysis import SyntaxAnalysis
from lexical.lexical_analysis import LexicalAnalysis
import tests.test_utils as u
import unittest

def readCode(file):
    code = ''
    code = open(file, "r")
    code_content = list(code.read())
    code.close()
    return code_content

class ConditionalExpressionsOperationsLoopTests(unittest.TestCase):

    def test_lexical_errors(self):
        code_content = list("""
            #

            ===

            =%

            123a
        """)
        is_valid = True
    
        al = LexicalAnalysis('', code_content, output=False)

        is_valid = is_valid and u.includes(al.errors[0].__str__(), 'unrecognized SYMBOL')            
        is_valid = is_valid and u.includes(al.errors[1].__str__(), 'unrecognized OPERATOR')            
        is_valid = is_valid and u.includes(al.errors[2].__str__(), 'unrecognized OPERATOR')            
        is_valid = is_valid and u.includes(al.errors[3].__str__(), 'unrecognized NUMBER')        

        self.assertTrue(is_valid)

    def test_lexical_empty_code(self):
        code_content = list('')
    
        al = LexicalAnalysis('', code_content, output=False)

        token = al.getNextToken()

        self.assertEqual(token, None)

if __name__ == '__main__':
    unittest.main()

    