from syntax.syntax_analysis import SyntaxAnalysis
from lexical.lexical_analysis import LexicalAnalysis
import unittest
import utils as u

def readCode(file):
    code = ''
    code = open(file, "r")
    code_content = list(code.read())
    code.close()
    return code_content

class ConditionalExpressionsOperationsLoopTests(unittest.TestCase):

    def test_should_pass_all_condition_cases(self):
        code_name = 'tests/tests_code/conditional_expression_operation_loop.c'
        code_content = readCode(code_name)
        al = LexicalAnalysis(code_name, code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertEqual(error, '')

    def test_should_raise_error_when_not_relational_operator(self):
        code_name = 'tests/tests_code/conditional_operator_error.c'
        code_content = readCode(code_name)
        al = LexicalAnalysis(code_name, code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'relational operator Expected'))

    def test_should_raise_error_when_no_opening_parenthesis(self):
        code_name = 'tests/tests_code/conditional_opening_parenthesis_error.c'
        code_content = readCode(code_name)
        al = LexicalAnalysis(code_name, code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'opening Parenthesis Expected'))

    def test_should_raise_error_when_no_closing_parenthesis(self):
        code_name = 'tests/tests_code/conditional_closing_parenthesis_error.c'
        code_content = readCode(code_name)
        al = LexicalAnalysis(code_name, code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'closing Parenthesis Expected'))

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

    