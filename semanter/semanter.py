# Semanter

from parser.parser import (ASTNode, ProgramNode, FunctionNode, BlockNode,
                             DeclarationNode, AssignmentNode, ConditionalNode, WhileNode,
                             PrintNode, FunctionCallNode, IdentifierNode, ConstantNode,
                             LiteralNode, BinaryOpNode)

class SemanticError(Exception):
    """Custom exception for semantic errors."""
    pass

class Symbol:
    def __init__(self, name, type, scope_level):
        self.name = name
        self.type = type
        self.scope_level = scope_level

class SymbolTable:
    def __init__(self):
        self._symbols = {}
        self._scope_stack = [{}]

    def enter_scope(self):
        self._scope_stack.append({})

    def exit_scope(self):
        if len(self._scope_stack) > 1:
            self._scope_stack.pop()
        else:
            raise SemanticError("Cannot exit global scope.")

    def declare(self, name, type):
        current_scope_level = len(self._scope_stack) - 1
        current_scope_symbols = self._scope_stack[-1]

        if name in current_scope_symbols:
            raise SemanticError(f"Identifier '{name}' already declared in the current scope.")

        symbol = Symbol(name, type, current_scope_level)
        current_scope_symbols[name] = symbol

    def lookup(self, name):
        for i in range(len(self._scope_stack) - 1, -1, -1):
            if name in self._scope_stack[i]:
                return self._scope_stack[i][name]
        return None

    def print_symbols(self):
        for scope in self._scope_stack:
            for name, symbol in scope.items():
                print(f"Name: {name}, Type: {symbol.type}, Scope Level: {symbol.scope_level}")
        print("End of Symbol Table")

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_function_return_type = None

    def analyze(self, ast_root: ProgramNode):
        if not isinstance(ast_root, ProgramNode):
            raise SemanticError("AST root must be a ProgramNode.")
        self.visit(ast_root)

    def visit(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    # Abstract method for nodes without a specific visit method
    def generic_visit(self, node: ASTNode):
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined and generic_visit not fully implemented for this node type.")

    def visit_ProgramNode(self, node: ProgramNode):
        # Functions are in the global scope
        for func_node in node.functions:
            if self.symbol_table.lookup(func_node.name) and self.symbol_table.lookup(func_node.name).scope_level == 0:
                raise SemanticError(f"Function '{func_node.name}' already declared.")
            self.symbol_table.declare(func_node.name, func_node.type_name)

        # Second pass: visit each function
        for func_node in node.functions:
            self.visit(func_node)

    def visit_FunctionNode(self, node: FunctionNode):
        # Check if function was already declared (e.g. in ProgramNode pass)
        func_symbol = self.symbol_table.lookup(node.name)
        if not func_symbol or func_symbol.type != node.type_name:
            raise SemanticError(f"Function '{node.name}' signature mismatch or not pre-declared.")

        self.current_function_return_type = node.type_name
        self.symbol_table.enter_scope()

        if node.block:
            if not isinstance(node.block, BlockNode):
                 raise SemanticError(f"Expected BlockNode for function '{node.name}' body, got {type(node.block)}.")
            for stmt in node.block.statements:
                self.visit(stmt)

        expected_return_type = self.current_function_return_type

        if node.return_expression is None:
            raise SemanticError(f"Non-void function '{node.name}' must return a value of type '{expected_return_type}'.")

        return_expr_type = self.visit(node.return_expression)
        if return_expr_type != expected_return_type:
            raise SemanticError(f"Return type mismatch in function '{node.name}'. Expected '{expected_return_type}' but got '{return_expr_type}'.")

        self.symbol_table.exit_scope()
        self.current_function_return_type = None

    def visit_BlockNode(self, node: BlockNode):
        self.symbol_table.enter_scope()
        for stmt in node.statements:
            self.visit(stmt)
        self.symbol_table.exit_scope()

    def visit_DeclarationNode(self, node: DeclarationNode):
        if node.type_name != 'int':
            raise SemanticError(f"Unsupported type '{node.type_name}'. Only 'int' is supported.")

        # Check for redeclaration
        self.symbol_table.declare(node.name, node.type_name)

        if node.expression:
            expr_type = self.visit(node.expression)
            if expr_type != node.type_name:
                raise SemanticError(f"Type mismatch in declaration of '{node.name}'. Expected '{node.type_name}' but got '{expr_type}'.")
        return node.type_name

    def visit_AssignmentNode(self, node: AssignmentNode):
        var_symbol = self.symbol_table.lookup(node.identifier_name)
        if not var_symbol:
            raise SemanticError(f"Identifier '{node.identifier_name}' not declared.")

        if var_symbol.type != 'int':
             raise SemanticError(f"Assignment to non-int variable '{node.identifier_name}' of type '{var_symbol.type}' is not supported or type error.")

        expr_type = self.visit(node.expression)
        if expr_type != var_symbol.type:
            raise SemanticError(f"Type mismatch in assignment to '{node.identifier_name}'. Expected '{var_symbol.type}' but got '{expr_type}'.")
        return var_symbol.type

    def visit_ConditionalNode(self, node: ConditionalNode):
        condition_type = self.visit(node.condition)
        # Non-zero integer is true and zero is false
        if condition_type != 'int':
            raise SemanticError(f"Condition for 'if' statement must be an 'int', got '{condition_type}'.")

        self.visit(node.if_block)
        if node.else_block:
            self.visit(node.else_block)

    def visit_WhileNode(self, node: WhileNode):
        condition_type = self.visit(node.condition)
        if condition_type != 'int':
            raise SemanticError(f"Condition for 'while' statement must be an 'int', got '{condition_type}'.")
        self.visit(node.block)

    def visit_PrintNode(self, node: PrintNode):
        expr_type = self.visit(node.expression)

        if isinstance(node.expression, LiteralNode):
            pass
        elif isinstance(node.expression, IdentifierNode):
            if expr_type != 'int':
                raise SemanticError(f"Identifier '{node.expression.name}' in print statement must be an 'int', got '{expr_type}'.")
        else:
            raise SemanticError(f"Unexpected expression type in print statement: {type(node.expression)}.")


    def visit_FunctionCallNode(self, node: FunctionCallNode):
        func_symbol = self.symbol_table.lookup(node.name)
        if not func_symbol:
            raise SemanticError(f"Function '{node.name}' not declared.")
        return func_symbol.type

    def visit_IdentifierNode(self, node: IdentifierNode):
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            raise SemanticError(f"Identifier '{node.name}' not declared.")
        return symbol.type

    def visit_ConstantNode(self, node: ConstantNode):
        try:
            int(node.value)
        except ValueError:
            raise SemanticError(f"Invalid integer constant: '{node.value}'.")
        return 'int'

    def visit_LiteralNode(self, node: LiteralNode):
        return 'string_literal'

    def visit_BinaryOpNode(self, node: BinaryOpNode):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != 'int' or right_type != 'int':
            raise SemanticError(f"Operands for binary operator '{node.operator}' must be 'int'. Got '{left_type}' and '{right_type}'.")

        return 'int'
