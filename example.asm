  str_7077823718609963935 db 72,101,108,108,111,33,10,0
  str_2576893828356663721 db 72,97,108,102,119,97,121,32,116,104,101,114,101,33,10,0
  str_412510102681959969 db 71,111,111,100,98,121,101,33,10,0
section .data
  newline db 0xA, 0      ; Newline character for Linux
  int_buffer times 12 db 0 ; Buffer for integer to string conversion (11 digits + sign + null)
section .text
global _start
hello:
  push ebp
  mov ebp, esp
  mov eax, 4          ; syscall: sys_write
  mov ebx, 1          ; fd: stdout
  mov ecx, str_7077823718609963935   ; message address
  mov edx, 7  ; message length
  int 0x80            ; Call kernel
  mov eax, 0   ; Return constant value
  mov esp, ebp      ; Deallocate locals
  pop ebp
  ret
_start:
  push ebp
  mov ebp, esp
  sub esp, 16  ; Allocate 16 bytes for locals: i, t1, t2, t3
  mov dword [ebp-4], 0
L1:
  mov eax, [ebp-4]
  mov ebx, 10
  cmp eax, ebx
  setl al         ; Set AL if less
  movzx eax, al   ; Zero-extend AL to EAX (EAX = 0 or 1)
  mov [ebp-8], eax
  mov eax, [ebp-8]
  test eax, eax    ; Test if the condition_var (result of a comparison) is zero
  je L2  ; Jump if condition_var is zero (false)
  call hello
  mov eax, [ebp-4]
  mov ebx, 5
  cmp eax, ebx
  sete al         ; Set AL if equal
  movzx eax, al   ; Zero-extend AL to EAX (EAX = 0 or 1)
  mov [ebp-12], eax
  mov eax, [ebp-12]
  test eax, eax    ; Test if the condition_var (result of a comparison) is zero
  je L3  ; Jump if condition_var is zero (false)
  mov eax, 4          ; syscall: sys_write
  mov ebx, 1          ; fd: stdout
  mov ecx, str_2576893828356663721   ; message address
  mov edx, 15  ; message length
  int 0x80            ; Call kernel
  jmp L4
L3:
  mov eax, [ebp-4]
  call print_integer
  call print_newline
L4:
  mov eax, [ebp-4]
  mov ebx, 1
  add eax, ebx
  mov [ebp-16], eax
  mov eax, [ebp-16]
  mov [ebp-4], eax
  jmp L1
L2:
  mov eax, 4          ; syscall: sys_write
  mov ebx, 1          ; fd: stdout
  mov ecx, str_412510102681959969   ; message address
  mov edx, 9  ; message length
  int 0x80            ; Call kernel
  ; --- Main function returning, preparing to exit ---
  mov ebx, 0 ; Exit code from main's return constant
  mov eax, 1            ; syscall: sys_exit
  int 0x80              ; Call kernel

; --- Helper Routines ---edi
print_integer:
  pusha             ; Save all general purpose registers
  mov edi, int_buffer
  add edi, 10       ; Point edi to where last char of number goes (buffer[10])
  mov byte [edi+1], 0 ; Null terminator at buffer[11]
  mov esi, edi        ; esi will track the start of the number string in buffer
                      ; For simplicity, if ebp is already saved by pusha, we can reuse it locally.
                      ; Let's assume ebp is safe to use here due to 'pusha' and will be restored by 'popa'.
  mov cl, 0          ; Flag: 0=positive, 1=negative (using ebp as it's saved by pusha)
  test eax, eax       ; Check if number is zero
  jne .print_int_check_negative
  mov byte [edi], '0' ; If zero, place '0'
  dec esi             ; Adjust esi to point to '0'
  jmp .print_int_do_print_num
.print_int_check_negative:
  jns .print_int_conversion_setup ; If positive, skip sign handling
  mov ebp, 1          ; Mark as negative (using ebp as flag)
  neg eax             ; Make eax positive for conversion
.print_int_conversion_setup:
  mov ebx, 10         ; Divisor for base 10
.print_int_convert_loop:
  xor edx, edx        ; Clear edx for division (edx:eax / ebx)
  div ebx             ; eax = quotient, edx = remainder
  add dl, '0'         ; Convert remainder (digit) to ASCII
  mov [edi], dl       ; Store ASCII digit in buffer
  dec edi             ; Move to previous char position in buffer
  dec esi             ; Adjust esi to point to the new first char
  test eax, eax       ; Is quotient zero?
  jnz .print_int_convert_loop ; If not, continue loop
  cmp ebp, 1          ; Was original number negative (ebp flag = 1)?
  jne .print_int_do_print_num ; If not negative, jump to print
  mov byte [edi], '-' ; Place '-' sign
  dec esi             ; Adjust esi to point to '-'
.print_int_do_print_num:
  inc esi             ; esi was decremented one last time, now points before the first char. Increment to point to it.
  mov ecx, esi        ; ecx = address of the string to print
  mov edx, int_buffer
  add edx, 11         ; edx = address of null terminator (one past last char)
  sub edx, esi        ; edx = length of the string (end - start)
  mov eax, 4          ; syscall: sys_write
  mov ebx, 1          ; fd: stdout
  int 0x80            ; Call kernel
  popa                ; Restore all registers (including original ebp)
  ret

print_newline:
  pusha
  mov eax, 4          ; syscall: sys_write
  mov ebx, 1          ; fd: stdout
  mov ecx, newline
  mov edx, 1          ; Length of newline character (just 0xA)
  int 0x80
  popa
  ret