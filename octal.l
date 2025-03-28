%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(const char *msg);
%}

%%
0[0-7]+          { printf("%s is an OCTAL number\n", yytext); }
0[xX][0-9a-fA-F]+ { printf("%s is a HEXADECIMAL number\n", yytext); }
[0-9]+           { printf("%s is a DECIMAL number\n", yytext); }
[ \t\n]          { /* Ignore whitespace */ }
.                { printf("Invalid input: %s\n", yytext); }
%%

int yywrap() {
    return 1;
}

int main() {
    printf("Enter a number: ");
    yylex();
    return 0;
}
