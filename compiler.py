import lexer.lexer as lexer
import parser.parser as parser
import semanter.semanter as semanter
import intermediator.intermediator as intermediator
import generator.generator as generator
import subprocess

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python compiler.py <source_file> <output_file>")
        sys.exit(1)

    source_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(source_file, 'r') as file:
            source_code = file.read()

        # Tokenize the source code
        lexer_instance = lexer.Lexer(source_code)
        tokens = lexer_instance.tokenize()

        # Print the tokens
        print("Tokens:")
        for token in tokens:
            print(token)

        # Parse the tokens
        parser_instance = parser.Parser(tokens)
        ast = parser_instance.parse_program()

        # Print the AST
        print("\nAbstract Syntax Tree (AST):")
        parser.print_ast(ast)

        # Run the semantic analysis
        semanter_instance = semanter.SemanticAnalyzer()
        semanter_instance.analyze(ast)

        # Generate Intermediate Code
        ir_generator = intermediator.IRGenerator()
        ir_code = ir_generator.generate(ast)

        # Print the Intermediate Code
        # print("\\nIntermediate Code:")
        for instruction in ir_code:
            print(instruction)

        # Call the code generator
        code_generator = generator.CodeGenerator(ir_code)
        code = code_generator.generate_x86()

        # Print the generated code
        asm_filename = output_file + ".asm"
        with open(asm_filename, "w") as asm_file:
            asm_file.write(code)
        print(f"\nGenerated x86 Assembly Code written to {asm_filename}")

        # asm code execution
        obj_filename = output_file + ".o"
        subprocess.run(["nasm", "-f", "elf32", asm_filename, "-o", obj_filename])
        subprocess.run(["ld", "-m", "elf_i386", obj_filename, "-o", output_file])

        print("\nProgram output:")

        result = subprocess.run(["./" + output_file], capture_output=True, text=True)
        print(result.stdout)

    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
        sys.exit(1)

