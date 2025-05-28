import lexer.lexer as lexer
import parser.parser as parser

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]

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

    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
        sys.exit(1)

