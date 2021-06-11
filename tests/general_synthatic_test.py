from compile import Compile
from syntax.syntax_analysis import SyntaxAnalysis
from lexical.lexical_analysis import LexicalAnalysis
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

if __name__ == '__main__':
    unittest.main()

    