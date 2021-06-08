from syntax.syntax_analysis import SyntaxAnalysis
from lexical.lexical_analysis import LexicalAnalysis
import unittest
import tests.test_utils as u

def readCode(file):
    code = ''
    code = open(file, "r")
    code_content = list(code.read())
    code.close()
    return code_content

class ConditionalExpressionsOperationsLoopTests(unittest.TestCase):

    def test_should_pass_all_condition_cases(self):
        code_content = list(""" 
            int main() {

                int a = 1, b = 2, x = 3, y = 4, c = 5;

                if (a == b) {

                    while ((x + 5) < y) {

                    }

                } else {
                    
                    while ((x + 5) < y) {
                        
                    }

                }

                while (x < 5) {

                }

                if (a == b && a == c) {

                }
                
                while (5 > x) {

                }

                if (a == b & a == c) {

                }


                if (a == b || a == c) {

                }

                while ((x + 5) < y) {
                    
                }

                if (a == b | a == c) {

                }
             }
        """)
        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertEqual(error, '')

    def test_should_raise_error_when_not_relational_operator(self):
        code_content = list("""
            int main() {

                int a = 1;
                int b = 5;

                if (a = b) {

                }

            }
        """)
        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'relational operator Expected'))

    def test_should_raise_error_when_no_opening_parenthesis(self):
        code_content = list("""
            int main() {

                int a = 1;
                int b = 1;

                if a == b) {

                }

            }
        """)
        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'opening Parenthesis Expected'))

    def test_should_raise_error_when_no_closing_parenthesis(self):
        code_content = list("""
            int main() {

                int a = 1;
                int b = 5;

                if (a == b {

                }

            }
        """)
        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'closing Parenthesis Expected'))

    def test_should_raise_error_when_no_opening_curly_after_else(self):
        code_content = list("""
            int main() {

                int a = 1;
                int b = 5;

                if (a == b) {

                } else

            }
        """)
        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertTrue(u.includes(error, 'opening curly braces Expected'))

if __name__ == '__main__':
    unittest.main()

    