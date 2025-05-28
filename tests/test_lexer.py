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
            if(x != y && x < y || x > y) {
                print("Complex condition");
            }
            return 0;
        }
        """
        lexer = Lexer(lexemes)
        tokens = lexer.tokenize()

        expected_tokens = [
            ('keyword', 'int'),
            ('identifier', 'main'),
            ('punctuation', '('),
            ('punctuation', ')'),
            ('punctuation', '{'),
            ('keyword', 'if'),
            ('punctuation', '('),
            ('identifier', 'a'),
            ('operator', '=='),
            ('identifier', 'b'),
            ('punctuation', ')'),
            ('punctuation', '{'),
            ('keyword', 'print'),
            ('punctuation', '('),
            ('literal', 'Hello, World!'),
            ('punctuation', ')'),
            ('punctuation', ';'),
            ('punctuation', '}'),
            ('keyword', 'else'),
            ('punctuation', '{'),
            ('keyword', 'print'),
            ('punctuation', '('),
            ('literal', 'Goodbye, World!'),
            ('punctuation', ')'),
            ('punctuation', ';'),
            ('punctuation', '}'),
            ('keyword', 'int'),
            ('identifier', 'x'),
            ('operator', '='),
            ('constant', '10'),
            ('punctuation', ';'),
            ('keyword', 'int'),
            ('identifier', 'y'),
            ('operator', '='),
            ('constant', '20'),
            ('punctuation', ';'),
            ('keyword', 'int'),
            ('identifier', 'z'),
            ('operator', '='),
            ('identifier', 'x'),
            ('operator', '+'),
            ('identifier', 'y'),
            ('punctuation', ';'),
            ('keyword', 'if'),
            ('punctuation', '('),
            ('identifier', 'x'),
            ('operator', '!='),
            ('identifier', 'y'),
            ('operator', '&&'),
            ('identifier', 'x'),
            ('operator', '<'),
            ('identifier', 'y'),
            ('operator', '||'),
            ('identifier', 'x'),
            ('operator', '>'),
            ('identifier', 'y'),
            ('punctuation', ')'),
            ('punctuation', '{'),
            ('keyword', 'print'),
            ('punctuation', '('),
            ('literal', 'Complex condition'),
            ('punctuation', ')'),
            ('punctuation', ';'),
            ('punctuation', '}'),
            ('keyword', 'return'),
            ('constant', '0'),
            ('punctuation', ';'),
            ('punctuation', '}')
        ]

        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(68, lexer.token_count())

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

        expected_tokens = [
            ('keyword', 'int'),
            ('identifier', 'main'),
            ('punctuation', '('),
            ('punctuation', ')'),
            ('punctuation', '{'),
            ('keyword', 'int'),
            ('identifier', 'x'),
            ('operator', '='),
            ('constant', '10'),
            ('punctuation', ';'),
            ('keyword', 'int'),
            ('identifier', 'y'),
            ('operator', '='),
            ('constant', '20'),
            ('punctuation', ';'),
            ('keyword', 'int'),
            ('identifier', 'z'),
            ('operator', '='),
            ('identifier', 'x'),
            ('operator', '+'),
            ('identifier', 'y'),
            ('punctuation', ';'),
            ('keyword', 'print'),
            ('punctuation', '('),
            ('identifier', 'x'),
            ('punctuation', ')'),
            ('punctuation', ';'),
            ('keyword', 'print'),
            ('punctuation', '('),
            ('identifier', 'y'),
            ('punctuation', ')'),
            ('punctuation', ';'),
            ('keyword', 'print'),
            ('punctuation', '('),
            ('identifier', 'z'),
            ('punctuation', ')'),
            ('punctuation', ';'),
            ('keyword', 'return'),
            ('constant', '0'),
            ('punctuation', ';'),
            ('punctuation', '}')
        ]

        self.assertEqual(tokens, expected_tokens)
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

        expected_tokens = [
            ('keyword', 'int'),
            ('identifier', 'main'),
            ('punctuation', '('),
            ('punctuation', ')'),
            ('punctuation', '{'),
            ('keyword', 'int'),
            ('identifier', 'intx'),
            ('operator', '='),
            ('constant', '10'),
            ('punctuation', ';'),
            ('keyword', 'int'),
            ('identifier', 'yint'),
            ('operator', '='),
            ('constant', '20'),
            ('punctuation', ';'),
            ('keyword', 'int'),
            ('identifier', 'zintz'),
            ('operator', '='),
            ('identifier', 'intx'),
            ('operator', '*'),
            ('identifier', 'yint'),
            ('punctuation', ';'),
            ('keyword', 'if'),
            ('punctuation', '('),
            ('identifier', 'intx'),
            ('operator', '<'),
            ('identifier', 'yint'),
            ('punctuation', ')'),
            ('punctuation', '{'),
            ('keyword', 'print'),
            ('punctuation', '('),
            ('literal', 'The number %d is less than %d'),
            ('punctuation', ','),
            ('identifier', 'intx'),
            ('punctuation', ','),
            ('identifier', 'yint'),
            ('punctuation', ')'),
            ('punctuation', ';'),
            ('punctuation', '}'),
            ('keyword', 'return'),
            ('constant', '0'),
            ('punctuation', ';'),
            ('punctuation', '}')
        ]

        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(43, lexer.token_count())

if __name__ == '__main__':
    unittest.main()
