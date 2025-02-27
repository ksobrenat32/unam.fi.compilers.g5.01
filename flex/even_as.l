/*
This program tests if a string contains an even number of 'a's.
*/

/* REGEX */
%%
([^a\n]*a[^a\n]*a)*[^a\n]*\n { printf("String contains an even number of 'a's.\n"); }
.*\n { printf("String does not contain an even number of 'a's.\n"); }
%%

int yywrap() { return 1; }

int main() {
    yylex();
    return 0;
}

