import unittest

from generator.generator import CodeGenerator
from intermediator.intermediator import (
    LabelInstr, AssignInstr, BinaryOpInstr, JumpInstr, ConditionalJumpInstr,
    ReturnInstr, FunctionCallInstr, PrintInstr
)


def normalize_asm(asm_code):
    """Normalizes assembly code for comparison.
    Strips leading/trailing whitespace from each line,
    and removes empty lines.
    """
    lines = [line.strip() for line in asm_code.splitlines()]
    return "\n".join(line for line in lines if line)


class TestCodeGenerator(unittest.TestCase):
    def setUp(self):
        # Generator is instantiated with ir_code per test
        pass

    def _run_generator(self, ir_instructions):
        generator = CodeGenerator(ir_instructions)
        return generator.generate_x86()

    def assertAsmEqual(self, generated_asm, expected_asm):
        self.assertEqual(normalize_asm(generated_asm), normalize_asm(expected_asm))

    def test_simple_return_constant(self):
        # IR for: int main() { return 0; }
        ir = [
            LabelInstr("main"),
            ReturnInstr(0)
        ]
        generated_asm = self._run_generator(ir)

        # Check that essential parts are present
        self.assertIn("section .data", generated_asm)
        self.assertIn("section .text", generated_asm)
        self.assertIn("global _start", generated_asm)
        self.assertIn("_start:", generated_asm)
        self.assertIn("push ebp", generated_asm)
        self.assertIn("mov ebp, esp", generated_asm)
        self.assertIn("mov ebx, 0", generated_asm)  # Exit code
        self.assertIn("mov eax, 1", generated_asm)  # sys_exit
        self.assertIn("int 0x80", generated_asm)

    def test_declaration_and_return_identifier(self):
        # IR for: int main() { int x = 10; return x; }
        ir = [
            LabelInstr("main"),
            AssignInstr("x", 10),
            ReturnInstr("x")
        ]
        generated_asm = self._run_generator(ir)

        # Check for variable allocation and access
        self.assertIn("sub esp, 4", generated_asm)  # Space for variable x
        self.assertIn("mov dword [ebp-4], 10", generated_asm)  # Assignment
        self.assertIn("mov eax, [ebp-4]", generated_asm)  # Loading x for return
        self.assertIn("mov ebx, eax", generated_asm)  # Exit code from variable

    def test_binary_operation_addition(self):
        # IR for: int main() { int t1 = 5 + 3; return t1; }
        ir = [
            LabelInstr("main"),
            BinaryOpInstr("t1", 5, "+", 3),
            ReturnInstr("t1")
        ]
        generated_asm = self._run_generator(ir)

        # Check arithmetic operation
        self.assertIn("mov eax, 5", generated_asm)
        self.assertIn("mov ebx, 3", generated_asm)
        self.assertIn("add eax, ebx", generated_asm)
        self.assertIn("mov [ebp-4], eax", generated_asm)  # Store result

    def test_binary_operation_subtraction(self):
        # IR for: int main() { int t1 = 10 - 3; return t1; }
        ir = [
            LabelInstr("main"),
            BinaryOpInstr("t1", 10, "-", 3),
            ReturnInstr("t1")
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("mov eax, 10", generated_asm)
        self.assertIn("mov ebx, 3", generated_asm)
        self.assertIn("sub eax, ebx", generated_asm)
        self.assertIn("mov [ebp-4], eax", generated_asm)

    def test_binary_operation_multiplication(self):
        # IR for: int main() { int t1 = 4 * 5; return t1; }
        ir = [
            LabelInstr("main"),
            BinaryOpInstr("t1", 4, "*", 5),
            ReturnInstr("t1")
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("mov eax, 4", generated_asm)
        self.assertIn("mov ebx, 5", generated_asm)
        self.assertIn("imul eax, ebx", generated_asm)
        self.assertIn("mov [ebp-4], eax", generated_asm)

    def test_binary_operation_division(self):
        # IR for: int main() { int t1 = 20 / 4; return t1; }
        ir = [
            LabelInstr("main"),
            BinaryOpInstr("t1", 20, "/", 4),
            ReturnInstr("t1")
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("mov eax, 20", generated_asm)
        self.assertIn("mov ebx, 4", generated_asm)
        self.assertIn("cdq", generated_asm)  # Sign extend
        self.assertIn("idiv ebx", generated_asm)
        self.assertIn("mov [ebp-4], eax", generated_asm)

    def test_binary_operation_comparison_equal(self):
        # IR for: int main() { int t1 = (5 == 5); return t1; }
        ir = [
            LabelInstr("main"),
            BinaryOpInstr("t1", 5, "==", 5),
            ReturnInstr("t1")
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("cmp eax, ebx", generated_asm)
        self.assertIn("sete al", generated_asm)
        self.assertIn("movzx eax, al", generated_asm)
        self.assertIn("mov [ebp-4], eax", generated_asm)

    def test_binary_operation_comparison_not_equal(self):
        # IR for: int main() { int t1 = (5 != 3); return t1; }
        ir = [
            LabelInstr("main"),
            BinaryOpInstr("t1", 5, "!=", 3),
            ReturnInstr("t1")
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("cmp eax, ebx", generated_asm)
        self.assertIn("setne al", generated_asm)
        self.assertIn("movzx eax, al", generated_asm)
        self.assertIn("mov [ebp-4], eax", generated_asm)

    def test_binary_operation_comparison_less_than(self):
        # IR for: int main() { int t1 = (3 < 5); return t1; }
        ir = [
            LabelInstr("main"),
            BinaryOpInstr("t1", 3, "<", 5),
            ReturnInstr("t1")
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("cmp eax, ebx", generated_asm)
        self.assertIn("setl al", generated_asm)
        self.assertIn("movzx eax, al", generated_asm)
        self.assertIn("mov [ebp-4], eax", generated_asm)

    def test_binary_operation_comparison_greater_than(self):
        # IR for: int main() { int t1 = (5 > 3); return t1; }
        ir = [
            LabelInstr("main"),
            BinaryOpInstr("t1", 5, ">", 3),
            ReturnInstr("t1")
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("mov eax, 5", generated_asm)
        self.assertIn("mov ebx, 3", generated_asm)
        self.assertIn("cmp eax, ebx", generated_asm)
        self.assertIn("setg al", generated_asm)
        self.assertIn("movzx eax, al", generated_asm)
        self.assertIn("mov [ebp-4], eax", generated_asm)

    def test_binary_operation_comparison_greater_equal(self):
        # IR for: int main() { int t1 = (5 >= 5); return t1; }
        ir = [
            LabelInstr("main"),
            BinaryOpInstr("t1", 5, ">=", 5),
            ReturnInstr("t1")
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("mov eax, 5", generated_asm)
        self.assertIn("mov ebx, 5", generated_asm)
        self.assertIn("cmp eax, ebx", generated_asm)
        self.assertIn("setge al", generated_asm)
        self.assertIn("movzx eax, al", generated_asm)
        self.assertIn("mov [ebp-4], eax", generated_asm)

    def test_binary_operation_comparison_less_equal(self):
        # IR for: int main() { int t1 = (3 <= 5); return t1; }
        ir = [
            LabelInstr("main"),
            BinaryOpInstr("t1", 3, "<=", 5),
            ReturnInstr("t1")
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("mov eax, 3", generated_asm)
        self.assertIn("mov ebx, 5", generated_asm)
        self.assertIn("cmp eax, ebx", generated_asm)
        self.assertIn("setle al", generated_asm)
        self.assertIn("movzx eax, al", generated_asm)
        self.assertIn("mov [ebp-4], eax", generated_asm)

    def test_print_integer_constant(self):
        # IR for: int main() { print(42); return 0; }
        ir = [
            LabelInstr("main"),
            PrintInstr(42),
            ReturnInstr(0)
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("mov eax, 42", generated_asm)
        self.assertIn("call print_integer", generated_asm)
        self.assertIn("call print_newline", generated_asm)
        self.assertIn("print_integer:", generated_asm)  # Helper routine included

    def test_print_integer_variable(self):
        # IR for: int main() { int val = 77; print(val); return 0; }
        ir = [
            LabelInstr("main"),
            AssignInstr("val", 77),
            PrintInstr("val"),
            ReturnInstr(0)
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("mov dword [ebp-4], 77", generated_asm)  # Store val
        self.assertIn("mov eax, [ebp-4]", generated_asm)  # Load val for print
        self.assertIn("call print_integer", generated_asm)

    def test_print_string_literal(self):
        # IR for: int main() { print("hello"); return 0; }
        ir = [
            LabelInstr("main"),
            PrintInstr('"hello"'),
            ReturnInstr(0)
        ]
        generated_asm = self._run_generator(ir)

        # Should contain string handling
        self.assertIn("str_", generated_asm)  # String label
        self.assertIn("mov eax, 4", generated_asm)  # sys_write
        self.assertIn("mov ebx, 1", generated_asm)  # stdout
        self.assertIn("mov edx, 5", generated_asm)  # Length of "hello"

    def test_conditional_jump_if_false(self):
        # IR for: if_false condition goto L1
        ir = [
            LabelInstr("main"),
            AssignInstr("condition", 0),
            ConditionalJumpInstr("condition", "L1", jump_if_false=True),
            AssignInstr("x", 1),
            LabelInstr("L1"),
            ReturnInstr(0)
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("test eax, eax", generated_asm)
        self.assertIn("je L1", generated_asm)  # Jump if false (zero)

    def test_conditional_jump_if_true(self):
        # IR for: if_true condition goto L1
        ir = [
            LabelInstr("main"),
            AssignInstr("condition", 1),
            ConditionalJumpInstr("condition", "L1", jump_if_false=False),
            AssignInstr("x", 1),
            LabelInstr("L1"),
            ReturnInstr(0)
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("test eax, eax", generated_asm)
        self.assertIn("jne L1", generated_asm)  # Jump if true (non-zero)

    def test_unconditional_jump(self):
        # IR for: goto L1
        ir = [
            LabelInstr("main"),
            JumpInstr("L1"),
            AssignInstr("x", 1),  # Should be skipped
            LabelInstr("L1"),
            ReturnInstr(0)
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("jmp L1", generated_asm)

    def test_function_call(self):
        # IR for: int main() { foo(); return 0; }
        # foo returns 42, but main doesn't use it.
        ir = [
            LabelInstr("foo"),
            ReturnInstr(42),
            LabelInstr("main"),
            FunctionCallInstr("foo"),
            ReturnInstr(0)
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("foo:", generated_asm)
        self.assertIn("_start:", generated_asm)
        self.assertIn("call foo", generated_asm)
        # Check foo's body
        self.assertIn("mov eax, 42", generated_asm)
        self.assertIn("mov ebx, 0", generated_asm)

    def test_data_section_generation(self):
        # Basic test to ensure data section is properly generated
        ir = [
            LabelInstr("main"),
            ReturnInstr(0)
        ]
        generated_asm = self._run_generator(ir)

        self.assertIn("section .data", generated_asm)
        self.assertIn("newline db 0xA, 0", generated_asm)
        self.assertIn("int_buffer times 12 db 0", generated_asm)

    def test_print_routines_included(self):
        # Test that helper routines are included
        ir = [
            LabelInstr("main"),
            PrintInstr(42),
            ReturnInstr(0)
        ]
        generated_asm = self._run_generator(ir)

        # Check for print_integer routine
        self.assertIn("print_integer:", generated_asm)
        self.assertIn("pusha", generated_asm)
        self.assertIn("popa", generated_asm)

        # Check for print_newline routine
        self.assertIn("print_newline:", generated_asm)


if __name__ == '__main__':
    unittest.main()
