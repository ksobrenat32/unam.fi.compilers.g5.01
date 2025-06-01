## Introduction

### Problem Formulation

In this project we need to design and implement a lexical analyzer as the first step of building a whole compiler.
The lexical analyzer must separate all file in a stream of tokens. Each token most follow a grammatical rule depending on his type, so first the lexer has to identify the type of tokens and then save it for the program output. For this project we design our lexer for a simple programming language based on C, which has a limited set of keywords, operators, constants, identifiers, literals and punctuation.

### Motivation

The tokens produced by the lexical analyzer essentially are the building blocks of our program. In the next steps of compilation we are going to validate the correct program structure using these building blocks, so the effectiveness of our compiler will depend directly on the correct work of the lexical analyzer.

### Objectives

Classify each token in the following categories:

- Keyword
- Identifier
- Operator
- Constant
- Literal
- Sign punctuation

The program output must show:

- Number of tokens
- Each identified token with his classification

## Technologies

We used Python as the main programming language for this project. We also used the following libraries:

- re
- unittest

## Theoretical Framework

A **lexeme** is a sequence of characters in the source program that matches the pattern for a token, and is identified by the lexical analyzer as an instance of that token. A **token** is a group of characters that logically belong together as the smallest unit in a compiler. The lexical analyzer groups the characters in the source program into tokens, and passes them to the parser. The parser uses the tokens to construct an abstract syntax tree.

For making the tokenization with essentially used the **re** library which gives the class re for designing regular expressions and then searching patterns in a text that fulfill those rules.

We concatenate all the regular expressions for each type of token in a single regex, so we can use it to search all the tokens in the source code at once. This is done by using the `|` operator to separate each regular expression.

We use `re.finditer()` to find all the matches of the regular expression in the source code. This method returns an iterator that yields match objects for each match found. We then iterate over the match objects and extract the token type and value from each match.


## Development

### Design Considerations

#### Keywords:

- if
- else
- while
- int
- return
- print

#### Operators:

- \+
- \-
- \*
- /
- =
- ==
- !=
- <
- \>
- <=
- \>=
- &&
- ||

#### Constants:

- [0-9]+

#### Identifiers:

- [a-zA-Z][a-zA-Z0-9_]*

#### Punctuation:

- (
- )
- {
- }
- ;
- ,

#### Comments:

- //.*

#### Literals:

- ".\*"
- '.\*'

### Implementation

The implementation of the lexical analyzer is done in the `lexer.py` file. The lexer is a class, which has a method `tokenize()` that takes a source code string as input and returns a list of tokens. The tokens are represented as a list of tuples, where each tuple contains the token type and the token value.

The `tokenize()` method uses the `re` library to find all the matches of the regular expression in the source code. It iterates over the match objects and extracts the token type and value from each match. The tokens are then added to a list, which is returned at the end of the method.

The lexer class also has a method `get_token_count()` that returns the number of tokens found in the source code. This method simply returns the length of the list of tokens.

## Results

As result we can say that the lexical analyzer works as expected. We have a series of test cases to show the behavior of the program. To run the tests, you can use the following command:

```bash
$ python -m unittest discover -s tests
```

If the output is `OK`, then all tests have passed successfully.

