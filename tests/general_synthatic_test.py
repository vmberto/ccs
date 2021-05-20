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
        code_content = list("""

            int main() {

                int x = 5;

        """)

        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
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
        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'unexpected end of file'))

    def test_should_raise_error_unexpected_token(self):
        code_content = list("""

            int main() {

                ==

            }

        """)   
        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'unexpected token'))

if __name__ == '__main__':
    unittest.main()

    