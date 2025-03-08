import unittest
from lexer.lexer import Lexer

class TestLexer(unittest.TestCase):
    def test_lexer_1(self):
        lexemes = """
        int main() {
            // This is a comment
            if(a == b) {
                prnt("Hello, World!");
            } else {
                prnt('Goodbye, World!');
            }
            int x = 10;
            int y = 20;
            int z = x + y;
            if(x >< y && x < y || x > y) {
                prnt("Complex condition");
            }
            return;
        }
        """
        lexer = Lexer(lexemes)
        tokens = lexer.tokenize()

        expected_tokens = {
            'keyword': ['int', 'if', 'prnt', 'else', 'prnt', 'int', 'int', 'int', 'if', 'prnt', 'return'],
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
            prnt(x);
            prnt(y);
            prnt(z);
            return 0;
        }
        """
        lexer = Lexer(lexemes)
        tokens = lexer.tokenize()

        expected_tokens = {
            'keyword': ['int', 'int', 'int', 'int', 'prnt', 'prnt', 'prnt', 'return'],
            'identifier': ['main', 'x', 'y', 'z', 'x', 'y', 'x', 'y', 'z'],
            'constant': ['10', '20', '0'],
            'operator': ['=', '=', '=', '+'],
            'punctuation': ['(', ')', '{', ';', ';', ';', '(', ')', ';', '(', ')', ';', '(', ')', ';' ,';', '}'],
            'unknown' : []
        }

        for key in expected_tokens:
            self.assertEqual(tokens[key], expected_tokens[key])

        self.assertEqual(41, lexer.token_count())

if __name__ == '__main__':
    unittest.main()
