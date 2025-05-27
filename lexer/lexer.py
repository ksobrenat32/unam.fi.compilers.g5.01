# Lexer

# Keywords:
# 0: if
# 1: else
# 3: int
# 4: return
# 5: print

# Operators:
# 1: +
# 2: -
# 3: *
# 4: /
# 5: =
# 6: ==
# 7: ><
# 8: <
# 9: >
# 10: <=
# 11: >=
# 12: &&
# 13: ||

# Constants:
# 1: [0-9]+

# Identifiers:
# 1: [a-zA-Z][a-zA-Z0-9]*

# Punctuation:
# 1: (
# 2: )
# 3: {
# 4: }
# 5: ;
# 6: ,

# Comments:
# 1: //.*

# Literals:
# 1: ".*"
# 2: '.*'

import re
from collections import defaultdict

class Lexer:
    lexemes = ""
    tokens = defaultdict(list)
    reserved = {}

    def __init__(self, lexemes) -> None:
        self.lexemes = lexemes
        self.tokens = defaultdict(list)

    def tokenize(self) -> defaultdict:
        # Divide the lexemes into tokens
        tokens = []

        # Remove comments
        lexemes = re.sub(r'//.*', '', self.lexemes)

        # Tokenize literals
        for token in re.findall(r'".*"', lexemes):
            self.tokens['literal'].append(token)
            lexemes = lexemes.replace(token, '')
        for token in re.findall(r"'.*'", lexemes):
            self.tokens['literal'].append(token)
            lexemes = lexemes.replace(token, '')

        # Tokenize identifiers
        for token in re.findall(r'[a-zA-Z][a-zA-Z0-9]*', lexemes):
            reserved = ['if', 'else', 'print', 'int', 'return']
            if token in reserved:
                self.tokens['keyword'].append(token)
            else:
                self.tokens['identifier'].append(token)
            lexemes = lexemes.replace(token, '')

        # Tokenize constants
        for token in re.findall(r'-?[0-9]+', lexemes):
            self.tokens['constant'].append(token)
            lexemes = lexemes.replace(token, '')

        # Tokenize operators
        for token in re.findall(r'==|><|<=|>=|[-+*/=<>]|&&|\|\|', lexemes):
            self.tokens['operator'].append(token)
            lexemes = lexemes.replace(token, '')

        # Tokenize punctuation
        for token in re.findall(r'[;{},()]', lexemes):
            self.tokens['punctuation'].append(token)
            lexemes = lexemes.replace(token, '')

        # Tokenize the rest
        for token in re.findall(r'[^a-zA-Z0-9]', lexemes):
            if token == ' ' or token == '\n':
                continue
            self.tokens['unknown'].append(token)

        return self.tokens

    def token_count(self) -> int:
        return sum(len(self.tokens[key]) for key in self.tokens)
