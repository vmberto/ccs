from syntax.syntax_analysis import SyntaxAnalysis
from lexical.lexical_analysis import LexicalAnalysis
import unittest

def readCode(file):
    code = ''
    code = open(file, "r")
    code_content = list(code.read())
    code.close()
    return code_content

class DeclarationAssingmentArithmeticTests(unittest.TestCase):

    def test_should_pass_all_declaration_assignment_arithmetic_cases(self):
        code_name = 'tests/tests_code/declaration_assignment_arithmetic.c'
        code_content = readCode(code_name)
        al = LexicalAnalysis(code_name, code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertEqual(error, '')


if __name__ == '__main__':
    unittest.main()