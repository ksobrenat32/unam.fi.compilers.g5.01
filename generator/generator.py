# Generator
import intermediator.intermediator as intermediator

class CodeGenerator:
    def __init__(self, ir_code):
        self.ir_code = ir_code
        self.assembly_code_parts = {
            "data": [],
            "text": []
        }
        self.var_locations = {}
        self.current_function_name = None
        self.current_function_var_offsets = {}
    # Constructor method of the CodeGenerator class that translates intermediate code to assembly code.

    def _get_var_location_or_value(self, var_name_or_value):
        if isinstance(var_name_or_value, int):
            return str(var_name_or_value)

        s_val = str(var_name_or_value)
        if s_val.isdigit() or (s_val.startswith('-') and s_val[1:].isdigit()):
            return s_val

        # Handle string literals (enclosed in single or double quotes)
        if (s_val.startswith('"') and s_val.endswith('"')) or (s_val.startswith("'") and s_val.endswith("'")):
            return s_val

        if var_name_or_value in self.current_function_var_offsets:
            return self.current_function_var_offsets[var_name_or_value]
        else:
            # This should ideally not be reached if pre-scan is correct and all vars are captured
            # For safety, we might allocate it here, but it's better to ensure all vars are known
            # at function entry.
            raise Exception(f"Variable {var_name_or_value} not found in allocations for function {self.current_function_name}.")
    # This method determines how to represent a variable or value in the assembly code.
    # When the input value is an integer, it simply converts it to a string.
    # If it is a variable name, it looks up the variable in self.current_function_var_offsets and returns its location.
    # If the variable is not found, it raises an exception.

    def _collect_vars_for_function(self, function_irs):
        local_vars = set() # Set to store unique local variables
        for instr in function_irs:
            if isinstance(instr, intermediator.AssignInstr):
                # This if statement checks if the target of the assignment is a variable (not a number)
                if not str(instr.target).isdigit(): local_vars.add(instr.target)
                if not isinstance(instr.source, int) and not str(instr.source).isdigit() and not str(instr.source).startswith('"') and not str(instr.source).startswith("'"):
                    local_vars.add(instr.source)
            elif isinstance(instr, intermediator.BinaryOpInstr):
                # This instruction checks if the target of the binary operation is a variable (not a number)
                if not str(instr.target).isdigit(): local_vars.add(instr.target)
                if not isinstance(instr.left, int) and not str(instr.left).isdigit() and not str(instr.left).startswith('"') and not str(instr.left).startswith("'"):
                    local_vars.add(instr.left)
                if not isinstance(instr.right, int) and not str(instr.right).isdigit() and not str(instr.right).startswith('"') and not str(instr.right).startswith("'"):
                    local_vars.add(instr.right)
            elif isinstance(instr, intermediator.ConditionalJumpInstr):
                # This instruction checks if the condition variable is a variable (not a number)
                if not isinstance(instr.condition_var, int) and not str(instr.condition_var).isdigit() and not str(instr.condition_var).startswith('"') and not str(instr.condition_var).startswith("'"):
                    local_vars.add(instr.condition_var)
            elif isinstance(instr, intermediator.ReturnInstr):
                # This instruction checks if the return value is a variable (not a number)
                if instr.value is not None and not isinstance(instr.value, int) and not str(instr.value).isdigit() and not str(instr.value).startswith('"') and not str(instr.value).startswith("'"):
                    local_vars.add(instr.value)
            elif isinstance(instr, intermediator.PrintInstr):
                # This instruction checks if the value to print is a variable (not a number)
                if not isinstance(instr.value, int) and not str(instr.value).isdigit() and not str(instr.value).startswith('"') and not str(instr.value).startswith("'"):
                    local_vars.add(instr.value)
        return sorted(list(local_vars)) # Ordena las variables locales y las devuelve como una lista
    # This method collects the local variables of a function from its intermediate code. It iterates through the instructions and adds the found variables to a set to avoid duplicates. Then, it returns a sorted list of these variables.

    def _get_irs_for_function(self, func_name_label):
        function_instructions = []
        in_function_scope = False # Flag to track if we are inside the function scope
        for i, instr in enumerate(self.ir_code): # Iterate through the IR code instructions
            # This checks if the instruction is a label and matches the function name label
            if isinstance(instr, intermediator.LabelInstr):
                if instr.name == func_name_label:
                    in_function_scope = True
                elif in_function_scope: # Reached another label, so previous function ended
                    break
            if in_function_scope:
                function_instructions.append(instr)
        return function_instructions
    # This method retrieves the intermediate code instructions for a specific function by its label name.

    def _add_asm(self, line, section="text"):
        self.assembly_code_parts[section].append(line)
    # This method adds a line of assembly code to the appropriate section (data or text) of the assembly code being generated.

    def generate_x86(self):
        # These three lines set up the necessary static data for later use in the assembly program, such as printing integers or handling newlines.
        self._add_asm("section .data")
        self._add_asm("  newline db 0xA, 0      ; Newline character for Linux")
        self._add_asm("  int_buffer times 12 db 0 ; Buffer for integer to string conversion (11 digits + sign + null)")

        # This section sets up the text segment where the actual code will be placed.
        self._add_asm("section .text", section="text")
        self._add_asm("global _start", section="text")

        # Iterate through functions first to set up stack frames and var offsets
        function_starts = {} # func_name -> index in ir_code
        for i, instr in enumerate(self.ir_code):
            if isinstance(instr, intermediator.LabelInstr) and not instr.name.startswith("L"): # Assuming function labels don't start with L (used for control flow)
                function_starts[instr.name] = i

        processed_functions = set()

        for func_name, start_index in function_starts.items():
            self.current_function_name = func_name
            self.current_function_var_offsets = {}

            # Extract IR for this function only
            func_irs = []
            for i in range(start_index, len(self.ir_code)):
                current_instr = self.ir_code[i]
                if isinstance(current_instr, intermediator.LabelInstr) and current_instr.name != func_name and current_instr.name in function_starts:
                    break # Reached the start of another function
                func_irs.append(current_instr)

            local_vars = self._collect_vars_for_function(func_irs)
            stack_size = len(local_vars) * 4 # 4 bytes per int variable

            label_to_emit = "_start" if func_name == "main" else func_name
            self._add_asm(f"{label_to_emit}:")
            self._add_asm("  push ebp")
            self._add_asm("  mov ebp, esp")
            if stack_size > 0:
                self._add_asm(f"  sub esp, {stack_size}  ; Allocate {stack_size} bytes for locals: {', '.join(local_vars)}")

            current_offset = 0
            for var_name in local_vars:
                current_offset += 4 # Stack grows downwards, so positive offsets from ebp are args, negative are locals
                self.current_function_var_offsets[var_name] = f"[ebp-{current_offset}]"

            # Now process instructions for this function
            for instr in func_irs:
                if isinstance(instr, intermediator.LabelInstr):
                    if instr.name != func_name: # Only emit non-function labels here
                         self._add_asm(f"{instr.name}:")
                # ... (rest of the instruction handling, adapted to use self.current_function_var_offsets)

                elif isinstance(instr, intermediator.AssignInstr):
                    target_loc = self._get_var_location_or_value(instr.target)
                    source_val_or_loc = self._get_var_location_or_value(instr.source)

                    if source_val_or_loc.startswith("[ebp-") or source_val_or_loc.startswith("[ebp+"):
                        self._add_asm(f"  mov eax, {source_val_or_loc}")
                        self._add_asm(f"  mov {target_loc}, eax")
                    else:
                        self._add_asm(f"  mov dword {target_loc}, {source_val_or_loc}")

                elif isinstance(instr, intermediator.BinaryOpInstr):
                    target_loc = self._get_var_location_or_value(instr.target)
                    left_val_or_loc = self._get_var_location_or_value(instr.left)
                    right_val_or_loc = self._get_var_location_or_value(instr.right)

                    if left_val_or_loc.startswith("[ebp-") or left_val_or_loc.startswith("[ebp+"):
                        self._add_asm(f"  mov eax, {left_val_or_loc}")
                    else:
                        self._add_asm(f"  mov eax, {left_val_or_loc}")

                    if right_val_or_loc.startswith("[ebp-") or right_val_or_loc.startswith("[ebp+"):
                        self._add_asm(f"  mov ebx, {right_val_or_loc}")
                    else:
                        self._add_asm(f"  mov ebx, {right_val_or_loc}")

                    op = instr.operator
                    if op == '+': self._add_asm("  add eax, ebx")
                    elif op == '-': self._add_asm("  sub eax, ebx")
                    elif op == '*': self._add_asm("  imul eax, ebx")
                    elif op == '/':
                        self._add_asm("  cdq           ; Sign extend eax into edx:eax for idiv")
                        self._add_asm("  idiv ebx      ; Quotient in eax, remainder in edx")
                    self._add_asm(f"  mov {target_loc}, eax")

                elif isinstance(instr, intermediator.JumpInstr):
                    self._add_asm(f"  jmp {instr.label_name}")

                elif isinstance(instr, intermediator.ConditionalJumpInstr):
                    condition_var_loc = self._get_var_location_or_value(instr.condition_var)
                    if condition_var_loc.startswith("[ebp-") or condition_var_loc.startswith("[ebp+"):
                        self._add_asm(f"  mov eax, {condition_var_loc}")
                    else:
                         self._add_asm(f"  mov eax, {condition_var_loc}")
                    self._add_asm("  cmp eax, 0")
                    if instr.jump_if_false:
                        self._add_asm(f"  je {instr.label_name}  ; Jump if condition is false (eax is 0)")
                    else:
                        self._add_asm(f"  jne {instr.label_name} ; Jump if condition is true (eax is not 0)")

                elif isinstance(instr, intermediator.ReturnInstr):
                    is_main_function = (self.current_function_name == "main")

                    if is_main_function:
                        self._add_asm("  ; --- Main function returning, preparing to exit ---")
                        if instr.value is not None:
                            val_or_loc = self._get_var_location_or_value(instr.value)
                            if val_or_loc.startswith("[ebp-") or val_or_loc.startswith("[ebp+"):
                                self._add_asm(f"  mov eax, {val_or_loc}")
                                self._add_asm(f"  mov ebx, eax        ; Exit code from main\'s return value")
                            else:
                                self._add_asm(f"  mov ebx, {val_or_loc} ; Exit code from main\'s return constant")
                        else:
                            self._add_asm("  xor ebx, ebx          ; Default exit code 0")
                        self._add_asm("  mov eax, 1            ; syscall: sys_exit")
                        self._add_asm("  int 0x80              ; Call kernel")
                    else:
                        if instr.value is not None:
                            val_or_loc = self._get_var_location_or_value(instr.value)
                            if val_or_loc.startswith("[ebp-") or val_or_loc.startswith("[ebp+"):
                                 self._add_asm(f"  mov eax, {val_or_loc}   ; Return value")
                            else:
                                 self._add_asm(f"  mov eax, {val_or_loc}   ; Return constant value")
                        # Epilogue for non-main functions
                        self._add_asm("  mov esp, ebp      ; Deallocate locals")
                        self._add_asm("  pop ebp")
                        self._add_asm("  ret")

                elif isinstance(instr, intermediator.PrintInstr):
                    val = instr.value
                    s_val = str(val)
                    # Check if it's a string literal
                    if (s_val.startswith('"') and s_val.endswith('"')) or (s_val.startswith("'") and s_val.endswith("'")):
                        # Remove quotes for label name
                        label_name = f'str_{abs(hash(s_val))}'
                        # Add string to data section if not already present
                        if label_name not in self.assembly_code_parts["data"]:
                            # Remove quotes and convert to comma-separated ASCII values
                            string_content = s_val[1:-1]
                            ascii_bytes = ', '.join(str(b) for b in string_content.encode("utf-8"))
                            self.assembly_code_parts["data"].append(f'  {label_name} db {ascii_bytes},0')
                        self._add_asm(f"  mov eax, 4          ; syscall: sys_write")
                        self._add_asm(f"  mov ebx, 1          ; fd: stdout")
                        self._add_asm(f"  mov ecx, {label_name}")
                        self._add_asm(f"  mov edx, {len(s_val) - 2}      ; length of string")
                        self._add_asm(f"  int 0x80")
                        self._add_asm("  call print_newline")
                    else:
                        val_or_loc = self._get_var_location_or_value(val)
                        if val_or_loc.startswith("[ebp-") or val_or_loc.startswith("[ebp+"):
                            self._add_asm(f"  mov eax, {val_or_loc}")
                        else:
                            self._add_asm(f"  mov eax, {val_or_loc}")
                        self._add_asm("  call print_integer")
                        self._add_asm("  call print_newline")

            processed_functions.add(func_name)
            # Ensure epilogue for main is handled by its ReturnInstr
            if func_name != "main" and not any(isinstance(ir, intermediator.ReturnInstr) for ir in func_irs):
                 # Add implicit return for void functions if not main and no explicit return
                self._add_asm("  mov esp, ebp")
                self._add_asm("  pop ebp")
                self._add_asm("  ret")

        # Add any remaining non-function labels (e.g. control flow labels not inside a processed function scope)
        # This might be redundant if all labels are handled within function scopes or are function labels themselves.
        # Consider if this is necessary based on IR structure.
        # For now, assuming all relevant labels are handled.

        self._append_print_routines()

        full_assembly = self.assembly_code_parts["data"] + self.assembly_code_parts["text"]
        return "\n".join(full_assembly)

    def _append_print_routines(self):
        self._add_asm("")
        self._add_asm("; --- Helper Routines ---edi")
        self._add_asm("print_integer:")
        self._add_asm("  pusha             ; Save all general purpose registers")
        self._add_asm("  mov edi, int_buffer")
        self._add_asm("  add edi, 10       ; Point edi to where last char of number goes (buffer[10])")
        self._add_asm("  mov byte [edi+1], 0 ; Null terminator at buffer[11]")
        self._add_asm("  mov esi, edi        ; esi will track the start of the number string in buffer")
        # self._add_asm("  mov ebp_print_flag, 0 ; Use a dedicated memory location or a non-clobbered reg if ebp is critical")
        self._add_asm("                      ; For simplicity, if ebp is already saved by pusha, we can reuse it locally.")
        self._add_asm("                      ; Let\'s assume ebp is safe to use here due to \'pusha\' and will be restored by \'popa\'.")
        self._add_asm("  mov cl, 0          ; Flag: 0=positive, 1=negative (using ebp as it\'s saved by pusha)")
        self._add_asm("  test eax, eax       ; Check if number is zero")
        self._add_asm("  jne .print_int_check_negative")
        self._add_asm("  mov byte [edi], \'0\' ; If zero, place \'0\'")
        self._add_asm("  dec esi             ; Adjust esi to point to \'0\'")
        self._add_asm("  jmp .print_int_do_print_num")
        self._add_asm(".print_int_check_negative:")
        self._add_asm("  jns .print_int_conversion_setup ; If positive, skip sign handling")
        self._add_asm("  mov ebp, 1          ; Mark as negative (using ebp as flag)")
        self._add_asm("  neg eax             ; Make eax positive for conversion")
        self._add_asm(".print_int_conversion_setup:")
        self._add_asm("  mov ebx, 10         ; Divisor for base 10")
        self._add_asm(".print_int_convert_loop:")
        self._add_asm("  xor edx, edx        ; Clear edx for division (edx:eax / ebx)")
        self._add_asm("  div ebx             ; eax = quotient, edx = remainder")
        self._add_asm("  add dl, \'0\'         ; Convert remainder (digit) to ASCII")
        self._add_asm("  mov [edi], dl       ; Store ASCII digit in buffer")
        self._add_asm("  dec edi             ; Move to previous char position in buffer")
        self._add_asm("  dec esi             ; Adjust esi to point to the new first char")
        self._add_asm("  test eax, eax       ; Is quotient zero?")
        self._add_asm("  jnz .print_int_convert_loop ; If not, continue loop")
        self._add_asm("  cmp ebp, 1          ; Was original number negative (ebp flag = 1)?")
        self._add_asm("  jne .print_int_do_print_num ; If not negative, jump to print")
        self._add_asm("  mov byte [edi], \'-\' ; Place \'-\' sign")
        self._add_asm("  dec esi             ; Adjust esi to point to \'-\'")
        self._add_asm(".print_int_do_print_num:")
        self._add_asm("  inc esi             ; esi was decremented one last time, now points before the first char. Increment to point to it.")
        self._add_asm("  mov ecx, esi        ; ecx = address of the string to print")
        self._add_asm("  mov edx, int_buffer")
        self._add_asm("  add edx, 11         ; edx = address of null terminator (one past last char)")
        self._add_asm("  sub edx, esi        ; edx = length of the string (end - start)")
        self._add_asm("  mov eax, 4          ; syscall: sys_write")
        self._add_asm("  mov ebx, 1          ; fd: stdout")
        self._add_asm("  int 0x80            ; Call kernel")
        self._add_asm("  popa                ; Restore all registers (including original ebp)")
        self._add_asm("  ret")
        self._add_asm("")
        self._add_asm("print_newline:")
        self._add_asm("  pusha")
        self._add_asm("  mov eax, 4          ; syscall: sys_write")
        self._add_asm("  mov ebx, 1          ; fd: stdout")
        self._add_asm("  mov ecx, newline")
        self._add_asm("  mov edx, 1          ; Length of newline character (just 0xA)")
        self._add_asm("  int 0x80")
        self._add_asm("  popa")
        self._add_asm("  ret")