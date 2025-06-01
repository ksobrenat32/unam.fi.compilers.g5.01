import unittest

from intermediator.intermediator import IRGenerator

from parser.parser import (
    ProgramNode, FunctionNode, BlockNode, DeclarationNode,
    AssignmentNode, ConditionalNode, PrintNode, IdentifierNode,
    ConstantNode, LiteralNode, BinaryOpNode, WhileNode
)

class TestIRGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = IRGenerator()

    def assert_ir_equals(self, generated_ir_objects, expected_ir_strings):
        generated_ir_strings = [str(instr) for instr in generated_ir_objects]
        self.assertEqual(generated_ir_strings, expected_ir_strings)

    def test_simple_return_constant(self):
        # AST for:
        # int main() {
        #   return 0;
        # }
        ast = ProgramNode(functions=[
            FunctionNode(
                type_name='int',
                name='main',
                block=BlockNode(statements=[]),
                return_expression=ConstantNode(value='0')
            )
        ])
        generated_ir = self.generator.generate(ast)
        expected_ir = [
            "main:",
            "  return 0"
        ]
        self.assert_ir_equals(generated_ir, expected_ir)

    def test_declaration_and_return_identifier(self):
        # AST for:
        # int main() {
        #   int x = 10;
        #   return x;
        # }
        ast = ProgramNode(functions=[
            FunctionNode(
                type_name='int',
                name='main',
                block=BlockNode(statements=[
                    DeclarationNode(type_name='int', name='x', expression=ConstantNode(value='10'))
                ]),
                return_expression=IdentifierNode(name='x')
            )
        ])
        generated_ir = self.generator.generate(ast)
        expected_ir = [
            "main:",
            "  x = 10",
            "  return x"
        ]
        self.assert_ir_equals(generated_ir, expected_ir)

    def test_binary_operation(self):
        # AST for:
        # int main() {
        #   int a = 5 + 3;
        #   return a;
        # }
        ast = ProgramNode(functions=[
            FunctionNode(
                type_name='int',
                name='main',
                block=BlockNode(statements=[
                    DeclarationNode(
                        type_name='int',
                        name='a',
                        expression=BinaryOpNode(
                            left=ConstantNode(value='5'),
                            operator='+',
                            right=ConstantNode(value='3')
                        )
                    )
                ]),
                return_expression=IdentifierNode(name='a')
            )
        ])
        generated_ir = self.generator.generate(ast)
        expected_ir = [
            "main:",
            "  t1 = 5 + 3",
            "  a = t1",
            "  return a"
        ]
        self.assert_ir_equals(generated_ir, expected_ir)

    def test_print_literal(self):
        # AST for:
        # int main() {
        #   print("hello");
        #   return 0;
        # }
        ast = ProgramNode(functions=[
            FunctionNode(
                type_name='int',
                name='main',
                block=BlockNode(statements=[
                    PrintNode(expression=LiteralNode(value='hello'))
                ]),
                return_expression=ConstantNode(value='0')
            )
        ])
        generated_ir = self.generator.generate(ast)
        expected_ir = [
            "main:",
            '  print "hello"',
            "  return 0"
        ]
        self.assert_ir_equals(generated_ir, expected_ir)

    def test_print_identifier(self):
        # AST for:
        # int main() {
        #   int val = 42;
        #   print(val);
        #   return 0;
        # }
        ast = ProgramNode(functions=[
            FunctionNode(
                type_name='int',
                name='main',
                block=BlockNode(statements=[
                    DeclarationNode(type_name='int', name='val', expression=ConstantNode(value='42')),
                    PrintNode(expression=IdentifierNode(name='val'))
                ]),
                return_expression=ConstantNode(value='0')
            )
        ])
        generated_ir = self.generator.generate(ast)
        expected_ir = [
            "main:",
            "  val = 42",
            "  print val",
            "  return 0"
        ]
        self.assert_ir_equals(generated_ir, expected_ir)

    def test_conditional_if_true(self):
        # AST for:
        # int main() {
        #   int x = 1;
        #   if (x == 1) { // condition is true
        #     x = 100;
        #   }
        #   return x;
        # }
        ast = ProgramNode(functions=[
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
                            AssignmentNode(identifier_name='x', expression=ConstantNode(value='100'))
                        ]),
                        else_block=None
                    )
                ]),
                return_expression=IdentifierNode(name='x')
            )
        ])
        generated_ir = self.generator.generate(ast)
        expected_ir = [
            "main:",
            "  x = 1",
            "  t1 = x == 1",
            "  if_false t1 goto L2",
            "  x = 100",
            "L2:",
            "  return x"
        ]
        self.assert_ir_equals(generated_ir, expected_ir)

    def test_conditional_if_else(self):
        # AST for:
        # int main() {
        #   int y = 0;
        #   if (y > 0) {
        #     y = 1;
        #   } else {
        #     y = -1;
        #   }
        #   return y;
        # }
        ast = ProgramNode(functions=[
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
        ])
        generated_ir = self.generator.generate(ast)
        expected_ir = [
            "main:",
            "  y = 0",
            "  t1 = y > 0",
            "  if_false t1 goto L1",
            "  y = 1",
            "  goto L2",
            "L1:",
            "  y = -1",
            "L2:",
            "  return y"
        ]
        self.assert_ir_equals(generated_ir, expected_ir)

    def test_while_loop(self):
        # AST for:
        # int main() {
        #   int count = 0;
        #   while (count < 3) {
        #     count = count + 1;
        #   }
        #   return count;
        # }
        ast = ProgramNode(functions=[
            FunctionNode(
                type_name='int',
                name='main',
                block=BlockNode(statements=[
                    DeclarationNode(type_name='int', name='count', expression=ConstantNode(value='0')),
                    WhileNode(
                        condition=BinaryOpNode(
                            left=IdentifierNode(name='count'),
                            operator='<',
                            right=ConstantNode(value='3')
                        ),
                        block=BlockNode(statements=[
                            AssignmentNode(
                                identifier_name='count',
                                expression=BinaryOpNode(
                                    left=IdentifierNode(name='count'),
                                    operator='+',
                                    right=ConstantNode(value='1')
                                )
                            )
                        ])
                    )
                ]),
                return_expression=IdentifierNode(name='count')
            )
        ])
        generated_ir = self.generator.generate(ast)
        expected_ir = [
            "main:",
            "  count = 0",
            "L1:",
            "  t1 = count < 3",
            "  if_false t1 goto L2",
            "  t2 = count + 1",
            "  count = t2",
            "  goto L1",
            "L2:",
            "  return count"
        ]
        self.assert_ir_equals(generated_ir, expected_ir)

    def test_empty_block_in_if(self):
        # AST for:
        # int main() {
        #   int x = 1;
        #   if (x > 0) {
        #     // empty block
        #   }
        #   return x;
        # }
        ast = ProgramNode(functions=[
            FunctionNode(
                type_name='int',
                name='main',
                block=BlockNode(statements=[
                    DeclarationNode(type_name='int', name='x', expression=ConstantNode(value='1')),
                    ConditionalNode(
                        condition=BinaryOpNode(
                            left=IdentifierNode(name='x'),
                            operator='>',
                            right=ConstantNode(value='0')
                        ),
                        if_block=BlockNode(statements=[]), # Empty if_block
                        else_block=None
                    )
                ]),
                return_expression=IdentifierNode(name='x')
            )
        ])
        generated_ir = self.generator.generate(ast)
        # L1: end_if_label
        # t1: result of x > 0
        expected_ir = [
            "main:",
            "  x = 1",
            "  t1 = x > 0",
            "  if_false t1 goto L2",
            # No instructions for empty if_block
            "L2:",
            "  return x"
        ]
        self.assert_ir_equals(generated_ir, expected_ir)

    def test_empty_block_in_while(self):
        # AST for:
        # int main() {
        #   int x = 0;
        #   while (x < 0) {
        #     // empty block
        #   }
        #   return x;
        # }
        ast = ProgramNode(functions=[
            FunctionNode(
                type_name='int',
                name='main',
                block=BlockNode(statements=[
                    DeclarationNode(type_name='int', name='x', expression=ConstantNode(value='0')),
                    WhileNode(
                        condition=BinaryOpNode(
                            left=IdentifierNode(name='x'),
                            operator='<',
                            right=ConstantNode(value='0')
                        ),
                        block=BlockNode(statements=[]) # Empty block
                    )
                ]),
                return_expression=IdentifierNode(name='x')
            )
        ])
        generated_ir = self.generator.generate(ast)
        expected_ir = [
            "main:",
            "  x = 0",
            "L1:",
            "  t1 = x < 0",
            "  if_false t1 goto L2",
            # No instructions for empty block
            "  goto L1",
            "L2:",
            "  return x"
        ]
        self.assert_ir_equals(generated_ir, expected_ir)

if __name__ == '__main__':
    unittest.main()
