%{
#include <stdio.h>
%}

%%

[a-z]    { printf("%c", yytext[0] - 32); }
[A-Z]    { printf("%c", yytext[0]); }
[\t\n]   ECHO;
.        ECHO;

%%

int yywrap() {
    return 1;
}

int main() {
    yylex();
    return 0;
}
