# Intermediator

# --- IR Node Classes ---
class IRInstruction:
    """Base class for all IR instructions."""
    def __str__(self):
        raise NotImplementedError

class LabelInstr(IRInstruction):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name}:"

class AssignInstr(IRInstruction):
    def __init__(self, target, source):
        self.target = target
        self.source = source
    def __str__(self):
        return f"  {self.target} = {self.source}"

class BinaryOpInstr(IRInstruction):
    def __init__(self, target, left, operator, right):
        self.target = target
        self.left = left
        self.operator = operator
        self.right = right
    def __str__(self):
        return f"  {self.target} = {self.left} {self.operator} {self.right}"

class JumpInstr(IRInstruction):
    def __init__(self, label_name):
        self.label_name = label_name
    def __str__(self):
        return f"  goto {self.label_name}"

class ConditionalJumpInstr(IRInstruction):
    def __init__(self, condition_var, label_name, jump_if_false=True):
        self.condition_var = condition_var
        self.label_name = label_name
        self.jump_if_false = jump_if_false
    def __str__(self):
        return f"  if_false {self.condition_var} goto {self.label_name}"

class ReturnInstr(IRInstruction):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"  return {self.value}"

class PrintInstr(IRInstruction):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"  print {self.value}"

# --- IR Generator Class ---
class IRGenerator:
    def __init__(self):
        self.ir_code = []
        self.label_count = 0
        self.temp_var_count = 0

    def _new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def _new_temp(self):
        self.temp_var_count += 1
        return f"t{self.temp_var_count}"

    def _add_instruction(self, instr):
        self.ir_code.append(instr)

    def _print_ir(self):
        """Utility method to print the generated IR code, useful for debugging."""
        for instr in self.ir_code:
            print(instr)

    def generate(self, node):
        """Public method to start IR generation from the root AST node."""
        self.ir_code = []
        self.label_count = 0
        self.temp_var_count = 0
        self._visit(node)
        return self.ir_code

    def _visit(self, node):
        """Helper method to dispatch to the correct visitor based on node type."""
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        self._print_ir()  # Print current IR for debugging
        raise Exception(f"No IRGenerator visitor method found for AST node type: {node.__class__.__name__}")

    def visit_ProgramNode(self, node):
        for func_node in node.functions:
            self._visit(func_node)

    def visit_FunctionNode(self, node):
        self._add_instruction(LabelInstr(node.name))

        self._visit(node.block)

        return_val_or_temp = self._visit(node.return_expression)
        self._add_instruction(ReturnInstr(return_val_or_temp))

    def visit_BlockNode(self, node):
        for stmt_node in node.statements:
            self._visit(stmt_node)

    def visit_DeclarationNode(self, node):
        if node.expression:
            expr_val_or_temp = self._visit(node.expression)
            self._add_instruction(AssignInstr(node.name, expr_val_or_temp))

    def visit_AssignmentNode(self, node):
        expr_val_or_temp = self._visit(node.expression)
        self._add_instruction(AssignInstr(node.identifier_name, expr_val_or_temp))

    def visit_ConditionalNode(self, node):
        condition_val_or_temp = self._visit(node.condition)

        else_label = self._new_label()
        end_if_label = self._new_label()

        # If condition_val_or_temp is 0 (false), jump to else_label (or end_if_label if no else_block)
        target_label_on_false = else_label if node.else_block else end_if_label
        self._add_instruction(ConditionalJumpInstr(condition_val_or_temp, target_label_on_false, jump_if_false=True))

        # If block (executes if condition was true)
        self._visit(node.if_block)

        if node.else_block:
            self._add_instruction(JumpInstr(end_if_label))
            self._add_instruction(LabelInstr(else_label))
            self._visit(node.else_block)
        else:
            if not node.else_block:
                 pass

        self._add_instruction(LabelInstr(end_if_label))

    def visit_WhileNode(self, node):
        loop_start_label = self._new_label()
        loop_end_label = self._new_label()

        self._add_instruction(LabelInstr(loop_start_label))
        condition_val_or_temp = self._visit(node.condition)

        # If condition_val_or_temp is 0 (false), jump out of the loop to loop_end_label
        self._add_instruction(ConditionalJumpInstr(condition_val_or_temp, loop_end_label, jump_if_false=True))

        # Loop body (executes if condition was true)
        self._visit(node.block)
        self._add_instruction(JumpInstr(loop_start_label))
        self._add_instruction(LabelInstr(loop_end_label))

    def visit_PrintNode(self, node):
        value_to_print = self._visit(node.expression)
        self._add_instruction(PrintInstr(value_to_print))

    def visit_IdentifierNode(self, node):
        return node.name

    def visit_ConstantNode(self, node):
        return node.value

    def visit_LiteralNode(self, node):
        return f'"{node.value}"'

    def visit_BinaryOpNode(self, node):
        left_operand = self._visit(node.left)
        right_operand = self._visit(node.right)

        result_temp = self._new_temp()
        self._add_instruction(BinaryOpInstr(result_temp, left_operand, node.operator, right_operand))
        return result_temp

