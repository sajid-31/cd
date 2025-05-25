import re
import pprint

# Sample source code
source_code = """
a = 3 + 5
b = a * 2
c = b - 4
d = c + 1

"""

# === Phase 1: Lexical Analysis ===
print("==== Phase 1: Lexical Analysis ====")

token_specification = [
    ('NUMBER',   r'\d+'),
    ('IDENT',    r'[a-zA-Z_]\w*'),
    ('ASSIGN',   r'='),
    ('OP',       r'[+\-*/]'),
    ('SKIP',     r'[ \t]+'),
    ('NEWLINE',  r'\n'),
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

tokens_by_line = []

for line_no, line in enumerate(source_code.strip().splitlines(), start=1):
    line_tokens = []
    for match in re.finditer(token_regex, line):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP':
            continue
        elif kind == 'NEWLINE':
            break
        else:
            line_tokens.append((kind, value))
    tokens_by_line.append((line_no, line.strip(), line_tokens))
    print(f"Line {line_no}: {line.strip()}")
    for token in line_tokens:
        print(f"  → {token[0]:<8} : {token[1]}")
print()

# === Phase 2: Syntax Analysis ===
print("==== Phase 2: Syntax Analysis (Parse Trees) ====")

def build_parse_tree(tokens):
    if len(tokens) == 3:
        return {
            'assign': {
                'lhs': tokens[0][1],
                'rhs': tokens[2][1]
            }
        }
    elif len(tokens) == 5:
        return {
            'assign': {
                'lhs': tokens[0][1],
                'rhs': {
                    'op': tokens[3][1],
                    'left': tokens[2][1],
                    'right': tokens[4][1]
                }
            }
        }
    else:
        return {'error': 'Syntax not supported'}

syntax_trees = []
for _, line_text, tokens in tokens_by_line:
    tree = build_parse_tree(tokens)
    syntax_trees.append(tree)
    print(f"Syntax Tree for: {line_text}")
    pprint.pprint(tree, indent=2)
    print()

# === Phase 3: Semantic Analysis ===
print("\n==== Phase 3: Semantic Analysis ====")

symbol_table = {}
for tree in syntax_trees:
    lhs = tree['assign']['lhs']
    rhs = tree['assign']['rhs']
    if isinstance(rhs, str):  # direct assignment
        if rhs.isdigit():
            symbol_table[lhs] = 'int'
        elif rhs.isidentifier():
            if rhs not in symbol_table:
                print(f"Semantic Error: Undefined variable {rhs}")
            symbol_table[lhs] = 'int'
    elif isinstance(rhs, dict):  # expression
        for operand in (rhs['left'], rhs['right']):
            if operand.isidentifier() and operand not in symbol_table:
                print(f"Semantic Error: Undefined variable {operand}")
        symbol_table[lhs] = 'int'
    print(f"{lhs} is of type int")

# === Phase 4: Intermediate Code Generation ===
print("\n==== Phase 4: Intermediate Code Generation ====")

temp_count = 1
intermediate_code = []

def get_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t

for tree in syntax_trees:
    lhs = tree['assign']['lhs']
    rhs = tree['assign']['rhs']
    if isinstance(rhs, str):
        intermediate_code.append(f"{lhs} = {rhs}")
    elif isinstance(rhs, dict):
        temp = get_temp()
        intermediate_code.append(f"{temp} = {rhs['left']} {rhs['op']} {rhs['right']}")
        intermediate_code.append(f"{lhs} = {temp}")

for code in intermediate_code:
    print(code)

# === Phase 5: Code Optimization (Constant Folding) ===
print("\n==== Phase 5: Code Optimization (Constant Folding) ====")

optimized_code = []
for code in intermediate_code:
    match = re.match(r"(t\d+) = (\d+) ([+\-*/]) (\d+)", code)
    if match:
        t, val1, op, val2 = match.groups()
        result = eval(f"{val1}{op}{val2}")
        optimized_code.append(f"{t} = {result}")
        print(f"Optimized: {code}  =>  {t} = {result}")
    else:
        optimized_code.append(code)

# === Phase 6: Target Code Generation ===
print("\n==== Phase 6: Target Code Generation ====")

register_count = 0

def get_reg():
    global register_count
    r = f"R{register_count}"
    register_count += 1
    return r

for code in optimized_code:
    parts = code.split('=')
    if len(parts) != 2:
        print(f"Skipping malformed line: {code}")
        continue

    left, right = map(str.strip, parts)
    tokens = right.split()

    if len(tokens) == 1:
        reg = get_reg()
        print(f"LOAD {reg}, {tokens[0]}")
        print(f"MOV {left}, {reg}")
    elif len(tokens) == 3:
        op1, op, op2 = tokens
        reg1 = get_reg()
        reg2 = get_reg()
        reg3 = get_reg()
        print(f"LOAD {reg1}, {op1}")
        print(f"LOAD {reg2}, {op2}")
        instr = {
            '+': "ADD",
            '-': "SUB",
            '*': "MUL",
            '/': "DIV"
        }.get(op, "UNKNOWN")
        print(f"{instr} {reg3}, {reg1}, {reg2}")
        print(f"MOV {left}, {reg3}")
    else:
        print(f"Unsupported expression: {right}")
