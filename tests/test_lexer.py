import unittest
from lexer.lexer import Lexer

class TestLexer(unittest.TestCase):
    def test_lexer_1(self):
        lexemes = """
        int main() {
            // This is a comment
            if(a == b) {
                print("Hello, World!");
            } else {
                print('Goodbye, World!');
            }
            int x = 10;
            int y = 20;
            int z = x + y;
            if(x >< y && x < y || x > y) {
                print("Complex condition");
            }
            return;
        }
        """
        lexer = Lexer(lexemes)
        tokens = lexer.tokenize()

        expected_tokens = {
            'keyword': ['int', 'if', 'print', 'else', 'print', 'int', 'int', 'int', 'if', 'print', 'return'],
            'identifier': ['main', 'a', 'b', 'x', 'y', 'z', 'x', 'y', 'x', 'y', 'x', 'y', 'x', 'y'],
            'constant': ['10', '20'],
            'operator': ['==', '=', '=', '=', '+', '><', '&&', '<', '||', '>'],
            'punctuation': ['(', ')', '{', '(', ')', '{', '(', ')', ';', '}', '{', '(', ')', ';', '}', ';', ';', ';', '(', ')', '{', '(', ')', ';', '}', ';', '}'],
            'literal': ['\"Hello, World!\"', '\"Complex condition\"', "'Goodbye, World!'"],
            'unknown': []
        }

        for key in expected_tokens:
            self.assertEqual(tokens[key], expected_tokens[key])

        self.assertEqual(67, lexer.token_count())

    def test_lexer_2(self):
        lexemes = """
        int main() {
            int x = 10;
            int y = 20;
            int z = x + y;
            print(x);
            print(y);
            print(z);
            return 0;
        }
        """
        lexer = Lexer(lexemes)
        tokens = lexer.tokenize()

        expected_tokens = {
            'keyword': ['int', 'int', 'int', 'int', 'print', 'print', 'print', 'return'],
            'identifier': ['main', 'x', 'y', 'z', 'x', 'y', 'x', 'y', 'z'],
            'constant': ['10', '20', '0'],
            'operator': ['=', '=', '=', '+'],
            'punctuation': ['(', ')', '{', ';', ';', ';', '(', ')', ';', '(', ')', ';', '(', ')', ';' ,';', '}'],
            'unknown' : []
        }

        for key in expected_tokens:
            self.assertEqual(tokens[key], expected_tokens[key])

        self.assertEqual(41, lexer.token_count())
        
    def test_lexer_3(self):
        lexemes = """
        int main() {
            int intx = 10;
            int yint = 20;
            int zintz = intx * yint;
            if(intx < yint ) {
                print("The number %d is less than %d", intx, yint);
            }
            return 0;
        }
        """
        lexer = Lexer(lexemes)
        tokens = lexer.tokenize()

        expected_tokens = {
            'keyword': ['int', 'int', 'int', 'int','if', 'print','return'],
            'identifier': ['main', 'intx', 'yint', 'zintz', 'intx', 'yint', 'intx', 'yint', 'intx', 'yint'],
            'constant': ['10', '20', '0'],
            'operator': ['=', '=', '=', '*','<'],
            'punctuation': ['(', ')', '{', ';', ';', ';', '(', ')','{' , '(', ',', ',',')',';', '}', ';', '}'],
            'unknown' : []
        }

        for key in expected_tokens:
            self.assertEqual(tokens[key], expected_tokens[key])

        self.assertEqual(43, lexer.token_count())

if __name__ == '__main__':
    unittest.main()
