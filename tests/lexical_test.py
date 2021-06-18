from ccs2.syntax.syntax_analysis import SyntaxAnalysis
from ccs2.lexical.lexical_analysis import LexicalAnalysis
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

            fd$
        """)
        is_valid = True
    
        al = LexicalAnalysis(code_content)

        is_valid = is_valid and u.includes(al.errors[0].__str__(), 'unrecognized SYMBOL')            
        is_valid = is_valid and u.includes(al.errors[1].__str__(), 'unrecognized OPERATOR')            
        is_valid = is_valid and u.includes(al.errors[2].__str__(), 'unrecognized OPERATOR')            
        is_valid = is_valid and u.includes(al.errors[3].__str__(), 'unrecognized NUMBER')   
        is_valid = is_valid and u.includes(al.errors[4].__str__(), 'Malformed Identifier')     

        self.assertTrue(is_valid)

    def test_lexical_tokens(self):
        code_content = list("""
            ==

            +

            ||

            123

            123.123

            'a'

            while

            variable

        """)
    
        al = LexicalAnalysis(code_content)


        self.assertEqual(al.getNextToken().getType(), 'Relational Operator')
        self.assertEqual(al.getNextToken().getType(), 'Arithmetic Operator')
        self.assertEqual(al.getNextToken().getType(), 'Conditional Operator')
        self.assertEqual(al.getNextToken().getType(), 'Integer')
        self.assertEqual(al.getNextToken().getType(), 'Float')
        self.assertEqual(al.getNextToken().getType(), 'Char')
        self.assertEqual(al.getNextToken().getType(), 'Reserved Word')
        self.assertEqual(al.getNextToken().getType(), 'Identifier')
        

    def test_lexical_empty_code(self):
        code_content = list('')
    
        al = LexicalAnalysis(code_content)

        token = al.getNextToken()

        self.assertEqual(token, None)

if __name__ == '__main__':
    unittest.main()

    