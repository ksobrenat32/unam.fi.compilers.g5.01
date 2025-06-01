import unittest

from lexer.lexer import Lexer
from parser.parser import Parser
from semanter.semanter import SemanticAnalyzer, SemanticError

class TestSemanticAnalyzer(unittest.TestCase):
    def analyze_code(self, code):
        """Helper method to lex, parse, and analyze code."""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)

    def analyze_code_for_error(self, code, expected_error_message_part):
        """Helper method to check for expected semantic errors."""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()
        analyzer = SemanticAnalyzer()
        with self.assertRaisesRegex(SemanticError, expected_error_message_part):
            analyzer.analyze(ast)

    def test_valid_simple_program(self):
        code = """
        int main() {
            return 0;
        }
        """
        self.analyze_code(code)

    def test_valid_program_with_declaration(self):
        code = """
        int main() {
            int x;
            x = 10;
            return x;
        }
        """
        self.analyze_code(code)

    def test_valid_program_with_declaration_and_initialization(self):
        code = """
        int main() {
            int x = 20;
            return x;
        }
        """
        self.analyze_code(code)

    def test_error_undeclared_variable_assignment(self):
        code = """
        int main() {
            x = 10; // x is not declared
            return 0;
        }
        """
        self.analyze_code_for_error(code, "Identifier 'x' not declared.")

    def test_error_undeclared_variable_return(self):
        code = """
        int main() {
            return x; // x is not declared
        }
        """
        self.analyze_code_for_error(code, "Identifier 'x' not declared.")

    def test_error_redeclaration_in_same_scope(self):
        code = """
        int main() {
            int x;
            int x; // Redeclaration
            return 0;
        }
        """
        self.analyze_code_for_error(code, "Identifier 'x' already declared in the current scope.")

    def test_valid_shadowing_in_nested_scope(self):
        code = """
        int main() {
            int x = 5;
            if (x == 5) {
                int x = 10; // Shadowing outer x
                print (x);
            }
            return x; // Should return 5
        }
        """
        self.analyze_code(code)

    def test_valid_binary_operation(self):
        code = """
        int main() {
            int a = 10;
            int b = 20;
            int c = a + b;
            return c;
        }
        """
        self.analyze_code(code)

    def test_error_binary_operation_on_undeclared_variable(self):
        code = """
        int main() {
            int a;
            a = 1 + b; // b is not declared
            return a;
        }
        """
        self.analyze_code_for_error(code, "Identifier 'b' not declared.")

    def test_valid_conditional_statement(self):
        code = """
        int main() {
            int x = 1 + 2 + 3;
            if (x == 10) {
                x = 20;
            } else {
                x = 30;
            }
            return x;
        }
        """
        self.analyze_code(code)

    def test_error_conditional_non_int_condition(self):
        code = """
        int main() {
            if (x == 10) { // x is not declared
                print("hello");
            }
            return 0;
        }
        """
        self.analyze_code_for_error(code, "Identifier 'x' not declared.")


    def test_valid_while_loop(self):
        code = """
        int main() {
            int i = 0;
            while (i < 5) {
                i = i + 1;
            }
            return i;
        }
        """
        self.analyze_code(code)

    def test_error_while_non_declared_variable(self):
        code = """
        int main() {
            while (x < 5) { // x is not declared
                print("looping");
            }
            return 0;
        }
        """
        self.analyze_code_for_error(code, "Identifier 'x' not declared.")

    def test_valid_print_identifier(self):
        code = """
        int main() {
            int val = 100;
            print(val);
            return 0;
        }
        """
        self.analyze_code(code)

    def test_valid_print_literal(self):
        code = """
        int main() {
            print("Hello World");
            return 0;
        }
        """
        self.analyze_code(code)

    def test_error_print_undeclared_identifier(self):
        code = """
        int main() {
            print(undeclared_var);
            return 0;
        }
        """
        self.analyze_code_for_error(code, "Identifier 'undeclared_var' not declared.")

    def test_valid_function_call(self):
        code = """
        int foo() {
            return 42;
        }
        int main() {
            foo(); // Call foo
            return 0;
        }
        """
        self.analyze_code(code)

    def test_error_calling_undeclared_function(self):
        code = """
        int main() {
            undeclared_func();
            return 0;
        }
        """
        self.analyze_code_for_error(code, "Function 'undeclared_func' not declared.")

    def test_valid_multiple_function_declarations(self):
        code = """
        int func1() {
            return 1;
        }
        int main() {
            return 0;
        }
        int func2() {
            return 2;
        }
        """
        self.analyze_code(code)

    def test_error_duplicate_function_declaration(self):
        code = """
        int main() {
            return 0;
        }
        int main() { // Duplicate
            return 1;
        }
        """
        self.analyze_code_for_error(code, "Function 'main' already declared.")

if __name__ == '__main__':
    unittest.main()
