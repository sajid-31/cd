import re

class IntermediateCodeGenerator:
    def __init__(self):
        self.temp_counter = 1
        self.tac_lines = []

    def get_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def precedence(self, op):
        if op in ['+', '-']:
            return 1
        if op in ['*', '/']:
            return 2
        return 0

    def infix_to_postfix(self, expr):
        output = []
        stack = []
        tokens = re.findall(r'\d+|[a-zA-Z_]\w*|[()+\-*/]', expr)
        for token in tokens:
            if re.match(r'\d+|[a-zA-Z_]\w*', token):
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                while stack and self.precedence(token) <= self.precedence(stack[-1]):
                    output.append(stack.pop())
                stack.append(token)
        while stack:
            output.append(stack.pop())
        return output

    def generate_tac_from_postfix(self, postfix):
        stack = []
        for token in postfix:
            if token not in '+-*/':
                stack.append(token)
            else:
                b = stack.pop()
                a = stack.pop()
                temp = self.get_temp()
                self.tac_lines.append(f"{temp} = {a} {token} {b}")
                stack.append(temp)
        return stack[0]

    def generate_tac(self, statement):
        statement = statement.replace(" ", "")
        if "=" in statement:
            var, expr = statement.split("=")
            postfix = self.infix_to_postfix(expr)
            final_temp = self.generate_tac_from_postfix(postfix)
            self.tac_lines.append(f"{var} = {final_temp}")
        else:
            print("Invalid statement!")

    def print_tac(self):
        for line in self.tac_lines:
            print(line)

def main():
    code_generator = IntermediateCodeGenerator()
    statements = [
        "a=(c+d)*4",
        "b=d*2",
        "y=z/2",
        "k=x%2"
    ]

    for statement in statements:
        code_generator.generate_tac(statement)
    code_generator.print_tac()

if __name__ == "__main__":
    main()
