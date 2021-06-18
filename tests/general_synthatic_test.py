from ccs2.compile import Compile
from ccs2.syntax.syntax_analysis import SyntaxAnalysis
from ccs2.lexical.lexical_analysis import LexicalAnalysis
import tests.test_utils as u
import unittest

class GeneralSynthaticTests(unittest.TestCase):

    def test_should_raise_error_unexpected_end_of_file(self):
        code_content = list("""

            int main() {

                int x = 5;

        """)

        error = ''
        try:
            Compile(code_content=code_content, testing=True)
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'unexpected end of file'))

    def test_should_raise_error_unexpected_end_of_file_other_case(self):
        code_content = list("""

            int main() {

                int x = 5;

                if (x == 5) {
                    
                }

        """)       

        error = ''

        try:
            Compile(code_content=code_content, testing=True)
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'unexpected end of file'))

    def test_should_raise_error_unexpected_token(self):
        code_content = list("""

            int main() {

                ==

            }

        """)   
        error = ''

        try:
            Compile(code_content=code_content, testing=True)
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'unexpected token'))

    def test_should_raise_error_int_declaration_expected(self):
        code_content = list("""
 

        """)   
        error = ''

        try:
            Compile(code_content=code_content, testing=True)
        except Exception as e:
            error = e.__str__()

        self.assertEqual('Syntax Error: type declaration for main identifier Expected', error)

    def test_should_raise_error_main_declaration_expected(self):
        code_content = list("""

            int 

        """)   
        error = ''

        try:
            Compile(code_content=code_content, testing=True)
        except Exception as e:
            error = e.__str__()

        self.assertEqual('Syntax Error: main identifier Expected', error)

    def test_should_raise_error_main_opening_parenthesis_declaration_expected(self):
        code_content = list("""

            int main 

        """)   
        error = ''

        try:
            Compile(code_content=code_content, testing=True)
        except Exception as e:
            error = e.__str__()

        self.assertEqual('Syntax Error: opening Parenthesis Expected', error)

    def test_should_raise_error_main_closing_parenthesis_declaration_expected(self):
        code_content = list("""

            int main(

        """)   
        error = ''

        try:
            Compile(code_content=code_content, testing=True)
        except Exception as e:
            error = e.__str__()

        self.assertEqual('Syntax Error: closing Parenthesis Expected', error)

if __name__ == '__main__':
    unittest.main()

    