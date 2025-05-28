import unittest
from lexer.lexer import Lexer
from parser.parser import (
    Parser, ProgramNode, FunctionNode, BlockNode, DeclarationNode,
    AssignmentNode, ConditionalNode, PrintNode, IdentifierNode,
    ConstantNode, LiteralNode, BinaryOpNode
)

class TestParser(unittest.TestCase):
    def assertASTEqual(self, node1, node2, msg=None):
        """Recursively checks if two AST nodes are equal."""
        if type(node1) != type(node2):
            raise self.failureException(f"Node types differ: {type(node1)} vs {type(node2)}. {msg or ''}")

        if isinstance(node1, ProgramNode):
            self.assertEqual(len(node1.functions), len(node2.functions), f"ProgramNode: Number of functions differ. {msg or ''}")
            for i in range(len(node1.functions)):
                self.assertASTEqual(node1.functions[i], node2.functions[i], f"ProgramNode: Function {i} differs. {msg or ''}")
        elif isinstance(node1, FunctionNode):
            self.assertEqual(node1.type_name, node2.type_name, f"FunctionNode: Type names differ for {node1.name}. {msg or ''}")
            self.assertEqual(node1.name, node2.name, f"FunctionNode: Names differ. {msg or ''}")
            self.assertASTEqual(node1.block, node2.block, f"FunctionNode: Blocks differ for {node1.name}. {msg or ''}")
            self.assertASTEqual(node1.return_expression, node2.return_expression, f"FunctionNode: Return expressions differ for {node1.name}. {msg or ''}")
        elif isinstance(node1, BlockNode):
            self.assertEqual(len(node1.statements), len(node2.statements), f"BlockNode: Number of statements differ. {msg or ''}")
            for i in range(len(node1.statements)):
                self.assertASTEqual(node1.statements[i], node2.statements[i], f"BlockNode: Statement {i} differs. {msg or ''}")
        elif isinstance(node1, DeclarationNode):
            self.assertEqual(node1.type_name, node2.type_name, f"DeclarationNode: Type names differ for {node1.name}. {msg or ''}")
            self.assertEqual(node1.name, node2.name, f"DeclarationNode: Names differ. {msg or ''}")
            if node1.expression or node2.expression: # Check expression only if one of them has it
                self.assertASTEqual(node1.expression, node2.expression, f"DeclarationNode: Expressions differ for {node1.name}. {msg or ''}")
        elif isinstance(node1, AssignmentNode):
            self.assertEqual(node1.identifier_name, node2.identifier_name, f"AssignmentNode: Identifier names differ. {msg or ''}")
            self.assertASTEqual(node1.expression, node2.expression, f"AssignmentNode: Expressions differ for {node1.identifier_name}. {msg or ''}")
        elif isinstance(node1, ConditionalNode):
            self.assertASTEqual(node1.condition, node2.condition, f"ConditionalNode: Conditions differ. {msg or ''}")
            self.assertASTEqual(node1.if_block, node2.if_block, f"ConditionalNode: If blocks differ. {msg or ''}")
            if node1.else_block or node2.else_block: # Check else_block only if one of them has it
                self.assertASTEqual(node1.else_block, node2.else_block, f"ConditionalNode: Else blocks differ. {msg or ''}")
        elif isinstance(node1, PrintNode):
            self.assertASTEqual(node1.expression, node2.expression, f"PrintNode: Expressions differ. {msg or ''}")
        elif isinstance(node1, IdentifierNode):
            self.assertEqual(node1.name, node2.name, f"IdentifierNode: Names differ. {msg or ''}")
        elif isinstance(node1, ConstantNode):
            self.assertEqual(node1.value, node2.value, f"ConstantNode: Values differ. {msg or ''}")
        elif isinstance(node1, LiteralNode):
            self.assertEqual(node1.value, node2.value, f"LiteralNode: Values differ. {msg or ''}")
        elif isinstance(node1, BinaryOpNode):
            self.assertASTEqual(node1.left, node2.left, f"BinaryOpNode: Left operands differ for operator {node1.operator}. {msg or ''}")
            self.assertEqual(node1.operator, node2.operator, f"BinaryOpNode: Operators differ. {msg or ''}")
            self.assertASTEqual(node1.right, node2.right, f"BinaryOpNode: Right operands differ for operator {node1.operator}. {msg or ''}")
        elif node1 is None and node2 is None:
            pass # Both are None, considered equal
        else:
            raise self.failureException(f"Unhandled node type or mismatch: {type(node1)} vs {type(node2)}. {msg or ''}")

    def test_simple_function(self):
        code = """
        int main() {
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[]),
                    return_expression=ConstantNode(value='0')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_function_with_declaration(self):
        code = """
        int main() {
            int x;
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        DeclarationNode(type_name='int', name='x', expression=None)
                    ]),
                    return_expression=ConstantNode(value='0')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_function_with_declaration_and_initialization(self):
        code = """
        int main() {
            int x = 10;
            return x;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        DeclarationNode(type_name='int', name='x', expression=ConstantNode(value='10'))
                    ]),
                    return_expression=IdentifierNode(name='x')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_function_with_assignment(self):
        code = """
        int main() {
            int x;
            x = 20;
            return x;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        DeclarationNode(type_name='int', name='x', expression=None),
                        AssignmentNode(identifier_name='x', expression=ConstantNode(value='20'))
                    ]),
                    return_expression=IdentifierNode(name='x')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_function_with_print_literal(self):
        code = """
        int main() {
            print("hello");
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        PrintNode(expression=LiteralNode(value='hello'))
                    ]),
                    return_expression=ConstantNode(value='0')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_function_with_print_identifier(self):
        code = """
        int main() {
            int message = 123;
            print(message);
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        DeclarationNode(type_name='int', name='message', expression=ConstantNode(value='123')),
                        PrintNode(expression=IdentifierNode(name='message'))
                    ]),
                    return_expression=ConstantNode(value='0')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_simple_if_statement(self):
        code = """
        int main() {
            int x = 1;
            if (x == 1) {
                x = 2;
            }
            return x;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        DeclarationNode(type_name='int', name='x', expression=ConstantNode(value='1')),
                        ConditionalNode(
                            condition=BinaryOpNode(
                                left=IdentifierNode(name='x'),
                                operator='==',
                                right=ConstantNode(value='1')
                            ),
                            if_block=BlockNode(statements=[
                                AssignmentNode(identifier_name='x', expression=ConstantNode(value='2'))
                            ]),
                            else_block=None
                        )
                    ]),
                    return_expression=IdentifierNode(name='x')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_if_else_statement(self):
        code = """
        int main() {
            int y = 0;
            if (y > 0) {
                y = 1;
            } else {
                y = -1;
            }
            return y;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        DeclarationNode(type_name='int', name='y', expression=ConstantNode(value='0')),
                        ConditionalNode(
                            condition=BinaryOpNode(
                                left=IdentifierNode(name='y'),
                                operator='>',
                                right=ConstantNode(value='0')
                            ),
                            if_block=BlockNode(statements=[
                                AssignmentNode(identifier_name='y', expression=ConstantNode(value='1'))
                            ]),
                            else_block=BlockNode(statements=[
                                AssignmentNode(identifier_name='y', expression=ConstantNode(value='-1'))
                            ])
                        )
                    ]),
                    return_expression=IdentifierNode(name='y')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_binary_expression(self):
        code = """
        int main() {
            int a = 10 + 5;
            return a;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        DeclarationNode(
                            type_name='int',
                            name='a',
                            expression=BinaryOpNode(
                                left=ConstantNode(value='10'),
                                operator='+',
                                right=ConstantNode(value='5')
                            )
                        )
                    ]),
                    return_expression=IdentifierNode(name='a')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_complex_expression(self):
        code = """
        int main() {
            int a = 1;
            int b = 2;
            int c = 3;
            int result = a + b * c;
            return result;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        # Current parser implementation is simple left-associative for all ops
        # So a + b * c becomes (a + b) * c
        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        DeclarationNode(type_name='int', name='a', expression=ConstantNode(value='1')),
                        DeclarationNode(type_name='int', name='b', expression=ConstantNode(value='2')),
                        DeclarationNode(type_name='int', name='c', expression=ConstantNode(value='3')),
                        DeclarationNode(
                            type_name='int',
                            name='result',
                            expression=BinaryOpNode(
                                left=BinaryOpNode(
                                    left=IdentifierNode(name='a'),
                                    operator='+',
                                    right=IdentifierNode(name='b')
                                ),
                                operator='*',
                                right=IdentifierNode(name='c')
                            )
                        )
                    ]),
                    return_expression=IdentifierNode(name='result')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_multiple_functions(self):
        code = """
        int helper() {
            return 42;
        }
        int main() {
            int val = 10;
            return val;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()

        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='helper',
                    block=BlockNode(statements=[]),
                    return_expression=ConstantNode(value='42')
                ),
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        DeclarationNode(type_name='int', name='val', expression=ConstantNode(value='10'))
                    ]),
                    return_expression=IdentifierNode(name='val')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_empty_block_in_if(self):
        code = """
        int main() {
            if (1 == 1) {}
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()
        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        ConditionalNode(
                            condition=BinaryOpNode(left=ConstantNode('1'), operator='==', right=ConstantNode('1')),
                            if_block=BlockNode(statements=[]),
                            else_block=None
                        )
                    ]),
                    return_expression=ConstantNode('0')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    def test_empty_block_in_if_else(self):
        code = """
        int main() {
            if (1 == 0) {} else {}
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse_program()
        expected_ast = ProgramNode(
            functions=[
                FunctionNode(
                    type_name='int',
                    name='main',
                    block=BlockNode(statements=[
                        ConditionalNode(
                            condition=BinaryOpNode(left=ConstantNode('1'), operator='==', right=ConstantNode('0')),
                            if_block=BlockNode(statements=[]),
                            else_block=BlockNode(statements=[])
                        )
                    ]),
                    return_expression=ConstantNode('0')
                )
            ]
        )
        self.assertASTEqual(ast, expected_ast)

    # --- SyntaxError Tests ---

    def test_error_missing_return_semicolon(self):
        code = """
        int main() {
            return 0
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, r"Expected value ; for token type punctuation but got }. at position 7."):
            parser.parse_program()

    def test_error_missing_closing_brace_function(self):
        code = """
        int main() {
            return 0;
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, r"Unexpected end of input. Expected punctuation with value }."):
            parser.parse_program()

    def test_error_no_functions(self):
        code = ""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, Parser._PROGRAM_MIN_ONE_FUNCTION):
            parser.parse_program()

    def test_error_declaration_missing_semicolon(self):
        code = """
        int main() {
            int x
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, r"Expected token type punctuation but got keyword value return. at position 7."):
             parser.parse_program()


    def test_error_assignment_missing_semicolon(self):
        code = """
        int main() {
            int x;
            x = 10
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, r"Expected token type punctuation but got keyword value return. at position 11."):
            parser.parse_program()

    def test_error_if_missing_closing_paren(self):
        code = """
        int main() {
            if (x == 1 {
                print("ok");
            }
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, r"Expected value \) for token type punctuation but got {. at position 10."):
            parser.parse_program()

    def test_error_print_missing_semicolon(self):
        code = """
        int main() {
            print("hello")
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, r"Expected token type punctuation but got keyword value return. at position 9."):
            parser.parse_program()

    def test_error_unexpected_token_in_block(self):
        code = """
        int main() {
            +
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, r"Unexpected token \+ type operator in block at position 5."):
            parser.parse_program()

    def test_error_expression_expected_identifier_constant_literal(self):
        code = """
        int main() {
            int x = +;
            return 0;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, r"Expected identifier or constant for expression got operator value \+ at position 8."):
            parser.parse_program()

    def test_error_return_missing_expression(self):
        code = """
        int main() {
            return ;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, r"Expected identifier or constant for expression got punctuation value ; at position 6."):
            parser.parse_program()


if __name__ == '__main__':
    unittest.main()
