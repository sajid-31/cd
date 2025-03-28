import re

def tokenize(expression):
    token_spec = [
        ('NUMBER', r'\d+'), ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'),
        ('ASSIGN', r':='), ('SEMI', r';'), ('LPAREN', r'\('), ('RPAREN', r'\)'),
        ('PLUS', r'\+'), ('MULT', r'\*'), ('MINUS', r'-'), ('DIV', r'/'),
        ('SKIP', r'[ \t]+'), ('NEWLINE', r'\n')
    ]
    tokens = [(m.lastgroup, m.group()) for m in re.finditer('|'.join(f'(?P<{t}>{r})' for t, r in token_spec), expression) if m.lastgroup not in ('SKIP', 'NEWLINE')]
    return tokens

class AdaParser:
    def __init__(self, tokens):  # FIXED: Corrected constructor name
        self.tokens, self.pos = tokens, 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token() and self.current_token()[0] == token_type:
            self.pos += 1
            return True
        return False

    def parse_factor(self):
        if self.eat('NUMBER') or self.eat('ID'):
            return {'Value': self.tokens[self.pos - 1][1]}
        if self.eat('LPAREN'):
            expr = self.parse_expression()
            if not self.eat('RPAREN'):
                raise SyntaxError("Missing closing parenthesis")
            return expr
        raise SyntaxError("Unexpected token")

    def parse_term(self):
        node = self.parse_factor()
        while self.eat('MULT') or self.eat('DIV'):
            node = {'Operator': self.tokens[self.pos - 1][1], 'Left': node, 'Right': self.parse_factor()}
        return node

    def parse_expression(self):
        node = self.parse_term()
        while self.eat('PLUS') or self.eat('MINUS'):
            node = {'Operator': self.tokens[self.pos - 1][1], 'Left': node, 'Right': self.parse_term()}
        return node

    def parse_assignment(self):
        if self.eat('ID'):
            var = self.tokens[self.pos - 1][1]
            if self.eat('ASSIGN'):
                expr = self.parse_expression()
                if not self.eat('SEMI'):
                    raise SyntaxError("Missing semicolon")
                return {'Assignment': {'Variable': var, 'Expression': expr}}
        raise SyntaxError("Invalid assignment")

    def parse(self):
        result = []
        while self.pos < len(self.tokens):
            result.append(self.format_tree(self.parse_assignment(), 0))
        return "\n".join(result)

    def format_tree(self, node, level):
        indent = ' ' * level
        if isinstance(node, (str, int)):  # FIXED: Handle strings correctly
            return f"{indent}{node}"
        return "\n".join(f"{indent}{k}:\n{self.format_tree(v, level + 1)}" for k, v in node.items())

# Example usage:
# expression = input("Enter the expression: ")
expression = "x := 5 + 3;"
try:
    tokens = tokenize(expression)
    parser = AdaParser(tokens)
    print(parser.parse())
except SyntaxError as e:
    print("Syntax Error:", e)
