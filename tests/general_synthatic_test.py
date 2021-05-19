from syntax.syntax_analysis import SyntaxAnalysis
from lexical.lexical_analysis import LexicalAnalysis
import utils as u
import unittest

def readCode(file):
    code = ''
    code = open(file, "r")
    code_content = list(code.read())
    code.close()
    return code_content

class ConditionalExpressionsOperationsLoopTests(unittest.TestCase):

    def test_should_raise_error_unexpected_end_of_file(self):
        code_name = 'tests/tests_code/general_unexpected_end_of_file_error.c'
        code_content = readCode(code_name)
        al = LexicalAnalysis(code_name, code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'unexpected end of file'))

    def test_should_raise_error_unexpected_end_of_file_other_case(self):
        code_name = 'tests/tests_code/general_unexpected_end_of_file_other_case_error.c'
        code_content = readCode(code_name)
        al = LexicalAnalysis(code_name, code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'unexpected end of file'))

    def test_should_raise_error_unexpected_token(self):
        code_name = 'tests/tests_code/general_unexpected_token_error.c'
        code_content = readCode(code_name)
        al = LexicalAnalysis(code_name, code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'unexpected token'))

    def test_should_raise_error_when_no_opening_parenthesis(self):
        code_name = 'tests/tests_code/conditional_else_without_curly_error.c'
        code_content = readCode(code_name)
        al = LexicalAnalysis(code_name, code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'opening curly braces Expected'))

if __name__ == '__main__':
    unittest.main()

    