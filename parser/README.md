## Introduction

### Problem Formulation

In this project we aim to design a syntax analyzer (also known as parser) for our C based programming language. The parser will take a stream of tokens produced by the lexical analyzer and validate the structure of the program according to the grammar rules defined for our language.

### Motivation

The parser is used as one of the middle steps of the compilation process. It is responsible for checking the syntactic correctness of the program and building an abstract syntax tree (AST) that represents the structure of the program. The effectiveness of the parser will directly impact the correctness and efficiency of the subsequent compilation steps.

### Objectives

Given a stream of tokens, the parser must:

- Validate the syntactic structure of the program according to the defined grammar rules.
- Build an abstract syntax tree (AST) that represents the structure of the program.
- Provide meaningful error messages when the syntax is incorrect.

## Technologies

The parser is implemented in pure Python, using the `unittest` framework for testing. The project structure is organized to separate the parser logic from the tests, making it easier to maintain and extend.

## Theoretical Framework

A parser is a component of a compiler that takes the tokens as input and converts it into a intermediate representation with the help of an existing grammar. The parser checks the syntax of the program and builds an abstract syntax tree (AST) that represents the structure of the program.

A **context-free grammar (CFG)** is a formal grammar that consists of a set of production rules that describe how to form strings from the language's alphabet. Each rule consists of a non-terminal symbol that can be replaced by a sequence of terminal and/or non-terminal symbols. The CFG is used to define the syntax of the programming language.

## Development

### Design Considerations

We can remember that this C based programming language is a simplified version of C, the limitations are:

- Only supports the 'int' type
- Functions don't accept parameters
- No loops (while, for) are defined
- No array or pointer support
- No function calls in expressions

#### Context-Free Grammar

The context-free grammar (CFG) for our C based programming language is defined as follows:

```
<grammar>
    <program> ::= <function> | <program> <function>
    <function> ::= <type> <identifier> '(' ')' '{' <block> 'return' <expression> ';' '}'
    <block> ::= <declaration> | <block> <declaration> | <statement> | <block> <statement> | <conditional> | <block> <conditional>
    <declaration> ::= <type> <identifier> ';' | <type> <identifier> '=' <expression> ';'
    <expression> ::= <identifier> | <constant> | <expression> <operator> <expression>
    <conditional> ::= 'if' '(' <expression> ')' '{' <block> '}' | 'if' '(' <expression> ')' '{' <block> '}' 'else' '{' <block> '}'
    <statement> ::= <identifier> '=' <expression> ';'
    <identifier> ::= <letter> | <letter> <name>
    <name> :: = <letter> | <digit> | <letter> <name> | <digit> <name>
    <type> ::= 'int'
    <constant> ::= <digit>
    <operator> ::= '+' | '-' | '*' | '/' | '==' | '><' | '<' | '>' | '<=' | '>=' | '&&' | '||'
    <letter> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
    <digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | <digit> <digit>
</grammar>
```

### Implementation

## Results

As result we can say that the lexical analyzer works as expected. We have a series of test cases to show the behavior of the program. To run the tests, you can use the following command:

```bash
$ python -m unittest discover -s tests
```

If the output is `OK`, then all tests have passed successfully.

## Conclusions

The parser has been successfully implemented and tested against a set of predefined test cases. It correctly validates the syntax of the C based programming language and builds an abstract syntax tree (AST) that represents the structure of the program. The parser also provides meaningful error messages when the syntax is incorrect, aiding in debugging and development.

## References

- S. GeeksforGeeks, "Types of Parsers in Compiler Design," [Online]. Available: https://www.geeksforgeeks.org/types-of-parsers-in-compiler-design/. [Accessed: 10-Jun-2024].
- S. GeeksforGeeks, "Problem on LR(0) Parser," [Online]. Available: https://www.geeksforgeeks.org/problem-on-lr0-parser/. [Accessed: 10-Jun-2024].
