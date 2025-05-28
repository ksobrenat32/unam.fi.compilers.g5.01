# Parser

# --- AST Nodes ---
class ASTNode:
    """Base class for all AST nodes."""
    pass

class ProgramNode(ASTNode):
    def __init__(self, functions):
        self.functions = functions # List of FunctionNode

class FunctionNode(ASTNode):
    def __init__(self, type_name, name, block, return_expression):
        self.type_name = type_name # str (e.g., 'int')
        self.name = name # str (identifier)
        self.block = block # BlockNode
        self.return_expression = return_expression # ExpressionNode

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements # List of DeclarationNode, AssignmentNode, ConditionalNode, PrintNode

class DeclarationNode(ASTNode):
    def __init__(self, type_name, name, expression=None):
        self.type_name = type_name # str (e.g., 'int')
        self.name = name # str (identifier)
        self.expression = expression # Optional: ExpressionNode (for initialization)

class AssignmentNode(ASTNode):
    def __init__(self, identifier_name, expression):
        self.identifier_name = identifier_name # str
        self.expression = expression # ExpressionNode

class ConditionalNode(ASTNode):
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition # ExpressionNode
        self.if_block = if_block # BlockNode
        self.else_block = else_block # Optional: BlockNode

class PrintNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression # ExpressionNode (can be IdentifierNode or LiteralNode)

# Expression Node Types
class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name # str

class ConstantNode(ASTNode):
    def __init__(self, value):
        self.value = value # str (representing an integer constant)

class LiteralNode(ASTNode):
    def __init__(self, value):
        self.value = value # str (e.g., "hello", \'world\')

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left # ExpressionNode
        self.operator = operator # str (e.g., '+', '==')
        self.right = right # ExpressionNode

# --- Parser Class ---
class Parser:
    def __init__(self, tokens: list[tuple[str, str]]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self) -> None:
        """Advance to the next token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def consume(self, expected_type: str, expected_value: str | None = None) -> tuple[str, str]:
        """Consume the current token if it matches expectations, or raise SyntaxError."""
        token = self.current_token
        if token is None:
            err_msg = f"Unexpected end of input. Expected {expected_type}"
            if expected_value:
                err_msg += f" with value \'{expected_value}\'"
            raise SyntaxError(err_msg)

        token_kind, token_value = token
        if token_kind != expected_type:
            raise SyntaxError(f"Expected token type \'{expected_type}\' but got \'{token_kind}\' (value: \'{token_value}\') at position {self.pos}")
        if expected_value is not None and token_value != expected_value:
            raise SyntaxError(f"Expected token \'{expected_type}:{expected_value}\' but got \'{token_kind}:{token_value}\' at position {self.pos}")

        self.advance()
        return token_kind, token_value

    def parse_program(self) -> ProgramNode:
        """<program> ::= <function>+"""
        functions = []
        while self.current_token is not None: # Program ends when no more tokens
            functions.append(self.parse_function())

        if not functions:
            raise SyntaxError("A program must contain at least one function.")
        return ProgramNode(functions)

    def parse_function(self) -> FunctionNode:
        """<function> ::= <type> <identifier> \'(\' \')\' \'{\' <block> \'return\' <expression> \';\' \'}\'"""
        type_name = self.parse_type()
        _, identifier_name = self.consume('identifier')
        self.consume('punctuation', '(')
        self.consume('punctuation', ')')
        self.consume('punctuation', '{')

        block = self.parse_block()

        self.consume('keyword', 'return')
        return_expression = self.parse_expression()
        self.consume('punctuation', ';')
        self.consume('punctuation', '}')

        return FunctionNode(type_name, identifier_name, block, return_expression)

    def parse_type(self) -> str:
        """<type> ::= 'int'"""
        _, type_val = self.consume('keyword', 'int')
        return type_val

    def parse_block(self) -> BlockNode:
        """<block> ::= { <declaration> | <statement> | <conditional> | <print_statement> }* """
        statements = []
        # A block continues until 'return' (for function body) or '}' (for if/else body)
        while (self.current_token is not None and
               not (self.current_token[0] == 'keyword' and self.current_token[1] == 'return') and
               not (self.current_token[0] == 'punctuation' and self.current_token[1] == '}')):

            current_kind, current_val = self.current_token
            if current_kind == 'keyword' and current_val == 'int':  # Start of a declaration
                statements.append(self.parse_declaration())
            elif current_kind == 'identifier':  # Start of an assignment statement
                statements.append(self.parse_statement())
            elif current_kind == 'keyword' and current_val == 'if':  # Start of a conditional
                statements.append(self.parse_conditional())
            elif current_kind == 'keyword' and current_val == 'print': # Start of a print statement
                statements.append(self.parse_print_statement())
            else:
                raise SyntaxError(f"Unexpected token \'{current_val}\' ({current_kind}) in block at position {self.pos}")

        return BlockNode(statements)

    def parse_declaration(self) -> DeclarationNode:
        """<declaration> ::= <type> <identifier> \';\' | <type> <identifier> \'=\' <expression> \';\'"""
        type_name = self.parse_type()
        _, identifier_name = self.consume('identifier')

        expression = None
        if self.current_token and self.current_token[0] == 'operator' and self.current_token[1] == '=':
            self.consume('operator', '=')
            expression = self.parse_expression()

        self.consume('punctuation', ';')
        return DeclarationNode(type_name, identifier_name, expression)

    def parse_statement(self) -> AssignmentNode:
        """<statement> ::= <identifier> \'=\' <expression> \';\'"""
        _, identifier_name = self.consume('identifier')
        self.consume('operator', '=')
        expression = self.parse_expression()
        self.consume('punctuation', ';')
        return AssignmentNode(identifier_name, expression)

    def parse_conditional(self) -> ConditionalNode:
        """<conditional> ::= 'if' \'(\' <expression> \')\' \'{\' <block> \'}\'
                         | 'if' \'(\' <expression> \')\' \'{\' <block> \'}\' 'else' \'{\' <block> \'}\'"""
        self.consume('keyword', 'if')
        self.consume('punctuation', '(')
        condition = self.parse_expression()
        self.consume('punctuation', ')')
        self.consume('punctuation', '{')
        if_block = self.parse_block() # parse_block stops at '}'
        self.consume('punctuation', '}')

        else_block = None
        if self.current_token and self.current_token[0] == 'keyword' and self.current_token[1] == 'else':
            self.consume('keyword', 'else')
            self.consume('punctuation', '{')
            else_block = self.parse_block() # parse_block stops at '}'
            self.consume('punctuation', '}')

        return ConditionalNode(condition, if_block, else_block)

    def parse_print_statement(self) -> PrintNode:
        """<print_statement> ::= 'print' \'(\' <literal> \')\' ';' | 'print' \'(\' <identifier> \')\' ';'"""
        self.consume('keyword', 'print')
        self.consume('punctuation', '(')
        if self.current_token is None:
            raise SyntaxError("Expected a literal or identifier after 'print(' at position {self.pos}")
        if self.current_token[0] == 'literal':
            _, literal_value = self.consume('literal')
            self.consume('punctuation', ')')
            self.consume('punctuation', ';')
            return PrintNode(LiteralNode(literal_value))
        elif self.current_token[0] == 'identifier':
            _, identifier_name = self.consume('identifier')
            self.consume('punctuation', ')')
            self.consume('punctuation', ';')
            return PrintNode(IdentifierNode(identifier_name))
        else:
            raise SyntaxError(f"Expected a literal or identifier after 'print(' at position {self.pos}, got {self.current_token[0]}:{self.current_token[1]}")

    def parse_simple_expression(self) -> ASTNode:
        """Parses the most basic elements of an expression: identifiers, constants, or literals.
           <simple_expression> ::= <identifier> | <constant> | <literal>
        """
        if not self.current_token:
            raise SyntaxError(f"Unexpected end of input. Expected identifier, constant, or literal at position {self.pos}")

        token_kind, token_value = self.current_token
        if token_kind == 'identifier':
            self.advance()
            return IdentifierNode(token_value)
        elif token_kind == 'constant':
            self.advance()
            return ConstantNode(token_value)
        elif token_kind == 'literal':
            self.advance()
            return LiteralNode(token_value)
        else:
            raise SyntaxError(f"Expected identifier, constant, or literal for expression, got {token_kind}:{token_value} at position {self.pos}")

    def parse_expression(self) -> ASTNode:
        """<expression> ::= <simple_expression> { <operator> <simple_expression> }*
           Handles left-associative binary operations.
           Operators from CFG: '+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=', '&&', '||'
           (Assuming '><' in CFG was a typo for '!=' as per lexer spec, or should be '!=' if lexer produces it)
        """
        node = self.parse_simple_expression()

        expression_operators = {'+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=', '&&', '||'}

        while (self.current_token and
               self.current_token[0] == 'operator' and
               self.current_token[1] in expression_operators):
            op_kind, op_value = self.current_token
            self.consume('operator', op_value) # Consume the operator
            right_node = self.parse_simple_expression()
            node = BinaryOpNode(node, op_value, right_node)

        return node

# Simple AST printer
def print_ast(node, indent=0):
    if node is None: return
    prefix = "  " * indent

    if isinstance(node, ProgramNode):
        print(f"ProgramNode:")
        for func in node.functions: print_ast(func, indent + 1)
    elif isinstance(node, FunctionNode):
        print(f"{prefix}FunctionNode: {node.name}() -> {node.type_name}")
        print(f"{prefix}  Block:")
        print_ast(node.block, indent + 2)
        print(f"{prefix}  Return:")
        print_ast(node.return_expression, indent + 2)
    elif isinstance(node, BlockNode):
        print(f"{prefix}BlockNode:")
        if not node.statements: print(f"{prefix}  (empty block)")
        for stmt in node.statements: print_ast(stmt, indent + 1)
    elif isinstance(node, DeclarationNode):
        print(f"{prefix}DeclarationNode: {node.name} ({node.type_name})")
        if node.expression:
            print(f"{prefix}  Initial Value:")
            print_ast(node.expression, indent + 1)
    elif isinstance(node, AssignmentNode):
        print(f"{prefix}AssignmentNode: {node.identifier_name} =")
        print_ast(node.expression, indent + 1)
    elif isinstance(node, ConditionalNode):
        print(f"{prefix}ConditionalNode:")
        print(f"{prefix}  Condition:")
        print_ast(node.condition, indent + 1)
        print(f"{prefix}  If True:")
        print_ast(node.if_block, indent + 1)
        if node.else_block:
            print(f"{prefix}  Else:")
            print_ast(node.else_block, indent + 1)
    elif isinstance(node, PrintNode):
        print(f"{prefix}PrintNode:")
        print_ast(node.expression, indent + 1)
    elif isinstance(node, IdentifierNode):
        print(f"{prefix}IdentifierNode: {node.name}")
    elif isinstance(node, ConstantNode):
        print(f"{prefix}ConstantNode: {node.value}")
    elif isinstance(node, LiteralNode):
        print(f"{prefix}LiteralNode: \\\"{node.value}\\\"")
    elif isinstance(node, BinaryOpNode):
        print(f"{prefix}BinaryOpNode: {node.operator}")
        print(f"{prefix}  Left:")
        print_ast(node.left, indent + 1)
        print(f"{prefix}  Right:")
        print_ast(node.right, indent + 1)
    else:
        print(f"{prefix}Unknown AST Node Type: {type(node)}")
