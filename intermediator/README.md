## Introduction

### Problem Formulation

In this project we are developing a Intermediate Representation (IR) generator (we decided to call it "intermediator" 😎) for a C based programming language. The IR generator will take an abstract syntax tree (AST) produced by the parser and convert it into an intermediate representation that can be used for further optimization and code generation.

### Motivation

Once we have a parser and the code is already semantically correct, the next step in the compilation process is to generate an intermediate representation (IR) of the program. The IR serves as a bridge between the high-level source code and the low-level machine code, allowing for optimizations and transformations that are independent of the target architecture.

### Objectives

The main objective of this project is to implement an IR generator that takes an AST as input and produces an intermediate representation of the program. The IR should be designed to be simple and easy to manipulate, while still being expressive enough to represent the semantics of the original program.

## Technologies

We will be using pure Python for the implementation of the IR generator.

## Theoretical Framework

### Intermediate Representation (IR)

An intermediate representation (IR) is a data structure or code that represents the program at an intermediate level between the high-level source code and the low-level machine code. The IR is designed to be easy to analyze and manipulate, allowing for optimizations and transformations that can improve the performance of the final generated code.

### Abstract Syntax Tree (AST)

An abstract syntax tree (AST) is a tree representation of the abstract syntactic structure of source code. Each node in the tree represents a construct occurring in the source code. The AST is generated by the parser and serves as the input for the IR generator.

### Semantic Analysis

Semantic analysis is the process of checking the semantic correctness of the program. It involves verifying that the program adheres to the rules of the language, such as type checking, scope resolution, and other language-specific constraints. The semantic analyzer will ensure that the AST is valid before it is passed to the IR generator.

### Code Generation

Code generation is the process of converting the intermediate representation into machine code or another lower-level representation that can be executed by a computer. The IR generator will produce an IR that can be further transformed and optimized before the final code generation step.

## Development

### Design Considerations

We can remember that this C based programming language is a simplified version of C, the limitations are:

- Only supports the 'int' type
- Functions don't accept parameters
- No loops for are defined
- No array or pointer support
- Our L1 tag is the main function, so it does not appear in the IR

The grammar of the language can be found in the `parser/README.md` file, which describes the syntax of the language. The semantic analyzer will use this grammar to validate the semantic correctness of the program.

### Implementation

The IR generator is implemented in the `intermediator` directory. The main components of the IR generator include:

- **IR Node Classes**: Classes that represent different types of IR nodes, such as expressions, statements, and control flow constructs.
- **IR Generator**: The main class that traverses the AST and generates the intermediate representation.
- **Visitor Pattern**: The IR generator uses the visitor pattern to traverse the AST and generate the corresponding IR nodes.
- **Error Handling**: The IR generator provides meaningful error messages when semantic errors are detected.

## References

- S. GeeksforGeeks, "Intermediate Code Generation in Compiler Design" [Online]. Available: https://www.geeksforgeeks.org/intermediate-code-generation-in-compiler-design/. [Accessed: 01-Jun-2025].

