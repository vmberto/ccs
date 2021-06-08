from syntax.syntax_analysis import SyntaxAnalysis
from lexical.lexical_analysis import LexicalAnalysis
import tests.test_utils as u
import unittest

class SemanticTests(unittest.TestCase):

    def test_should_raise_typing_error_float_int(self):
        code_content = list("""

            int main() {

                int a = 3;

                a = 2;

                int b = 3 / a;
            
            }
        """)

        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertEqual(error, 'Semantic Error: Variable (b) of type int with floating point value (1.5)')

    def test_should_raise_typing_error_float_int_other_case(self):
        code_content = list("""

            int main() {

                int a = 5;

                a = 1.5;

            }

        """)

        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertEqual(error, 'Semantic Error: Variable (a) of type int with floating point value (1.5)')

    def test_should_raise_undeclared_variable_error(self):
        code_content = list("""

            int main() {

                a = 5;

            }

        """)

        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertEqual(error, 'Semantic Error: Variable a undeclared')

    def test_should_raise_unintialized_variable_error(self):
        code_content = list("""

            int main() {

                int a = 5, b;

                if (b < 5) {
                    
                }

            }

        """)

        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertEqual(error, 'Semantic Error: Variable (b) was declared but not initialized')

    def test_should_raise_unintialized_variable_error_other_case(self):
        code_content = list("""

            int main() {

                int a = 5, b;

                a = 50 + b;

            }

        """)

        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertEqual(error, 'Semantic Error: Variable (b) was declared but not initialized')

    def test_should_raise_already_declared_variable(self):
        code_content = list("""

            int main() {

                int a = 5, a = 8;

            }

        """)

        al = LexicalAnalysis('', code_content, output=False)
        error = ''

        try:
            SyntaxAnalysis(al).execute()
        except Exception as e:
            error = e.__str__()

        self.assertEqual(error, 'Semantic Error: Variable a already declared')

    def test_should_pass_same_variable_different_scope(self):
        code_content = list("""

            int main() {

                int a = 5;

                if (a == 5) {
                    int a = 10;
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


if __name__ == '__main__':
    unittest.main()

    