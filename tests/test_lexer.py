import unittest
from lexer.lexer import Lexer

class TestLexer(unittest.TestCase):
    def test_empty_input(self):
        lexer = Lexer("")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [])
        self.assertEqual(lexer.token_count(), 0)

    def test_whitespace_only(self):
        lexer = Lexer(" \n\t  ")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [])
        self.assertEqual(lexer.token_count(), 0)

    def test_comments_only(self):
        lexer = Lexer("// This is a comment\\n// Another comment")
        tokens = lexer.tokenize()
        self.assertEqual(tokens, [])
        self.assertEqual(lexer.token_count(), 0)

    def test_all_keywords(self):
        source = "if else print int return"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_tokens = [
            ('keyword', 'if'),
            ('keyword', 'else'),
            ('keyword', 'print'),
            ('keyword', 'int'),
            ('keyword', 'return')
        ]
        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(lexer.token_count(), 5)

    def test_all_operators(self):
        source = "+ - * / = == != < > <= >= && ||"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_tokens = [
            ('operator', '+'),
            ('operator', '-'),
            ('operator', '*'),
            ('operator', '/'),
            ('operator', '='),
            ('operator', '=='),
            ('operator', '!='),
            ('operator', '<'),
            ('operator', '>'),
            ('operator', '<='),
            ('operator', '>='),
            ('operator', '&&'),
            ('operator', '||')
        ]
        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(lexer.token_count(), 13)

    def test_integer_constants_variations(self):
        source = "0 123 -45 007"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_tokens = [
            ('constant', '0'),
            ('constant', '123'),
            ('constant', '-45'),
            ('constant', '007')
        ]
        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(lexer.token_count(), 4)

    def test_identifier_variations(self):
        source = "a _myVar var123 another_ID _1"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_tokens = [
            ('identifier', 'a'),
            ('identifier', '_myVar'),
            ('identifier', 'var123'),
            ('identifier', 'another_ID'),
            ('identifier', '_1')
        ]
        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(lexer.token_count(), 5)

    def test_string_literal_variations(self):
        source = '"" "hello" \'\' \'world\' "with space" \'also with space\''
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_tokens = [
            ('literal', ''),
            ('literal', 'hello'),
            ('literal', ''),
            ('literal', 'world'),
            ('literal', 'with space'),
            ('literal', 'also with space')
        ]
        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(lexer.token_count(), 6)

    def test_punctuation(self):
        source = "; { } ( ) ,"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_tokens = [
            ('punctuation', ';'),
            ('punctuation', '{'),
            ('punctuation', '}'),
            ('punctuation', '('),
            ('punctuation', ')'),
            ('punctuation', ',')
        ]
        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(lexer.token_count(), 6)

    def test_mismatched_characters(self):
        source = "int a = 5 @ 10;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_tokens = [
            ('keyword', 'int'),
            ('identifier', 'a'),
            ('operator', '='),
            ('constant', '5'),
            ('unknown', '@'),
            ('constant', '10'),
            ('punctuation', ';')
        ]
        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(lexer.token_count(), 7)

    def test_no_space_between_tokens(self):
        source = "if(a==b)x=y+z;"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_tokens = [
            ('keyword', 'if'),
            ('punctuation', '('),
            ('identifier', 'a'),
            ('operator', '=='),
            ('identifier', 'b'),
            ('punctuation', ')'),
            ('identifier', 'x'),
            ('operator', '='),
            ('identifier', 'y'),
            ('operator', '+'),
            ('identifier', 'z'),
            ('punctuation', ';')
        ]
        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(lexer.token_count(), 12)

    def test_mixed_comments_and_code(self):
        source = """
        // Start of program
        int main() { // main function
            print("hello"); // print statement
            // return 0;
        } // end of main
        // End of program
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected_tokens = [
            ('keyword', 'int'),
            ('identifier', 'main'),
            ('punctuation', '('),
            ('punctuation', ')'),
            ('punctuation', '{'),
            ('keyword', 'print'),
            ('punctuation', '('),
            ('literal', 'hello'),
            ('punctuation', ')'),
            ('punctuation', ';'),
            ('punctuation', '}')
        ]
        self.assertEqual(tokens, expected_tokens)
        self.assertEqual(lexer.token_count(), 11)

    def test_general_text_1(self):
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
        self.assertEqual(68, lexer.token_count())\

    def test_general_text_2(self):
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

    def test_general_text_3(self):
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
