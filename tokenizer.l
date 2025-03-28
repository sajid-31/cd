%{
#include <stdio.h>
#include <string.h>

void print_tr(const char *token, const char *type) {
    for(int i=0; i<strlen(token); i++) {
        printf("%c", token[i]);
        if(i < strlen(token) - 1) printf("->");
    }
    printf("->%s\n", type);
}
%}

%%

"int"|"float"|"if"|"else"|"return"|"while" { print_tr(yytext, "keyword"); }
"+"|"-"|"*"|"/"|"="|"=="|"!="|"<"|">" { print_tr(yytext, "operator"); }
"("|")"|"{"|"}"|";"|"," { print_tr(yytext, "special_symbol"); }
[a-zA-Z_][a-zA-Z0-9_]* { print_tr(yytext, "identifier"); }
[0-9]+ { print_tr(yytext, "constant"); }
[\t\n] {}    // skip whitespace

%%

int main() {
    yylex();
    return 0;
}

int yywrap() { return 1; }
