# Lexer

# Keywords:
# 0: if
# 1: else
# 3: int
# 4: return
# 5: print
# 6: while

# Operators:
# 1: +
# 2: -
# 3: *
# 4: /
# 5: =
# 6: ==
# 7: !=
# 8: <
# 9: >
# 10: <=
# 11: >=
# 12: &&
# 13: ||

# Constants:
# 1: -?[0-9]+

# Identifiers:
# 1: [a-zA-Z_][a-zA-Z0-9_]*

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
class Lexer:
    def __init__(self, source_code: str) -> None:
        self.source_code = source_code
        self.tokens_list: list[tuple[str, str]] | None = None

    def tokenize(self) -> list[tuple[str, str]]:
        token_specification = [
            ('COMMENT',      r'//[^\n]*'), # Comments
            ('LITERAL',      r'"[^"]*"|\'[^\']*\''), # String literals (e.g., "abc", 'xyz')
            ('KEYWORD',      r'\b(if|else|print|int|return|while)\b'), # Keywords
            ('IDENTIFIER',   r'[a-zA-Z_][a-zA-Z0-9_]*'), # Identifiers (e.g., var_name, myFunction)
            ('CONSTANT',     r'-?[0-9]+'), # Integer constants (e.g., 123, 0, -5)
            ('OPERATOR',     r'==|!=|<=|>=|&&|\|\||[-+*/=<>]'), # Operators
            ('PUNCTUATION',  r'[;{},()]'), # Punctuation
            ('WHITESPACE',   r'\s+'), # Whitespace
            ('MISMATCH',     r'.') # Any other character (error token)
        ]
        # Combine all regex patterns into one, using named capture groups
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

        self.tokens_list = []

        for mo in re.finditer(tok_regex, self.source_code):
            kind = mo.lastgroup
            value = mo.group()

            if kind == 'COMMENT' or kind == 'WHITESPACE':
                # Skip comments and whitespace
                continue

            token_value = value
            if kind == 'LITERAL':
                # For string literals, remove the surrounding quotes
                token_value = value[1:-1]

            if kind == 'MISMATCH':
                # Handle unexpected characters
                self.tokens_list.append(('unknown', token_value))
            else:
                # For all other valid tokens, store as (lowercase_type, value)
                self.tokens_list.append((kind.lower(), token_value))

        return self.tokens_list

    def token_count(self) -> int:
        if self.tokens_list is None:
            # If tokenize() hasn't been called, there are no tokens
            return 0
        return len(self.tokens_list)
