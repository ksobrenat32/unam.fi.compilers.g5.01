## Introduction

### Problem Formulation

In this project we are designing a semantic analyzer (we decided to call it "semanter") for our C based programming language. The semantic analyzer will take an abstract syntax tree (AST) produced by the parser and validate the semantic correctness of the program according to the rules defined for our language.

### Motivation

Through the compiling process, the semantic analyzer is responsible for checking the semantic correctness of the program and ensuring that the program adheres to the rules of the language. The effectiveness of the semantic analyzer will directly impact the correctness and efficiency of the subsequent compilation steps.

### Objectives

Given an abstract syntax tree (AST), the semantic analyzer must:

- Validate the semantic structure of the program according to the defined rules.
- Provide meaningful error messages when the semantics are incorrect.
- Generate a symbol table that contains information about the identifiers used in the program.

## Technologies

The semantic analyzer is implemented in pure Python, using the `unittest` framework for testing. The project structure is organized to separate the semantic analysis logic from the tests, making it easier to maintain and extend.

## Theoretical Framework

A semantic analyzer is a component of a compiler that takes the abstract syntax tree (AST) as input and checks the semantic correctness of the program. It ensures that the program adheres to the rules of the language, such as type checking, scope resolution, and identifier resolution.

A **symbol table** is a data structure used by the semantic analyzer to store information about identifiers in the program. It maps identifiers to their attributes, such as type, scope, and location. The symbol table is used to check for semantic errors, such as undeclared variables or type mismatches.

Some of the functions that the semantic analyzer performs include:

- **Type Checking**: Ensuring that operations are performed on compatible types.
- **Scope Resolution**: Ensuring that identifiers are declared before they are used and that they are used in the correct scope.
- **Identifier Resolution**: Ensuring that identifiers are unique within their scope and that they are not used before declaration.
- **Flow Analysis**: Ensuring that the control flow of the program is valid, such as checking for unreachable code or ensuring that all paths return a value.

## Development

### Design Considerations

We can remember that this C based programming language is a simplified version of C, the limitations are:

- Only supports the 'int' type
- Functions don't accept parameters
- No loops for are defined
- No array or pointer support

The grammar of the language can be found in the `parser/README.md` file, which describes the syntax of the language. The semantic analyzer will use this grammar to validate the semantic correctness of the program.

### Implementation

The semantic analyzer is implemented in the `semanter` directory. The main components of the semantic analyzer include:
- **Symbol Table**: A data structure to store information about identifiers.
- **Semantic Analyzer**: The main class that performs semantic analysis on the AST.
- **Visitor Pattern**: The semantic analyzer uses the visitor pattern to traverse the AST and perform semantic checks.
- **Error Handling**: The semantic analyzer provides meaningful error messages when semantic errors are detected.

## Results

## Conclusions

## References

- S. GeeksforGeeks, "Semantic Analysis in Compiler Design," [Online]. Available: https://www.geeksforgeeks.org/semantic-analysis-in-compiler-design/. [Accessed: 28-May-2025].
- S. Pgrandinetti, "How to Design Semantic Analysis," [Online]. Available: https://pgrandinetti.github.io/compilers/page/how-to-design-semantic-analysis/. [Accessed: 28-May-2025].
- S. Tutorialspoint, "Compiler Design Semantic Analysis," [Online]. Available: https://www.tutorialspoint.com/compiler_design/compiler_design_semantic_analysis.htm. [Accessed: 28-May-2025].
