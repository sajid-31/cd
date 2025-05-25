import pandas as pd
class LL1Parser:
    def __init__(self, grammar, terminals: set):
        self.grammar = grammar
        self.terminals = terminals
        self.non_terminals = list(grammar.keys())
        self.first_sets = {nt: set() for nt in self.non_terminals}
        self.follow_sets = {nt: set() for nt in self.non_terminals}
        self.parsing_table = {}

    def compute_first(self, symbol):
        if symbol not in self.non_terminals:
            return {symbol}

        if self.first_sets[symbol]:
            return self.first_sets[symbol]

        first = set()
        for prod in self.grammar[symbol]:
            for s in prod:
                if s == 'ε':
                    first.add('ε')
                    break
                first_s = self.compute_first(s)
                first.update(first_s - {'ε'})
                if 'ε' not in first_s:
                    break
            else:
                first.add('ε')

        self.first_sets[symbol] = first
        return first

    def compute_follow(self, symbol):
        if not self.follow_sets[symbol]:
            if symbol == self.non_terminals[0]:  # Start symbol
                self.follow_sets[symbol].add('$')

            for lhs in self.grammar:
                for prod in self.grammar[lhs]:
                    if symbol in prod:
                        idx = prod.index(symbol) + 1
                        while idx < len(prod):
                            next_symbol = prod[idx]
                            first_next = self.compute_first(next_symbol)
                            self.follow_sets[symbol].update(first_next - {'ε'})
                            if 'ε' not in first_next:
                                break
                            idx += 1
                        else:
                            if lhs != symbol:
                                self.follow_sets[symbol].update(self.compute_follow(lhs))

        return self.follow_sets[symbol]

    def construct_parse_table(self):
        for nt in self.non_terminals:
            self.compute_first(nt)
            self.compute_follow(nt)

        # Initialize the table
        for nt in self.non_terminals:
            self.parsing_table[nt] = {}
            for t in self.terminals.union({'$'}):
                self.parsing_table[nt][t] = ""

        # Fill table
        for nt in self.non_terminals:
            for prod in self.grammar[nt]:
                first = set()
                if prod[0] == 'ε':
                    first.add('ε')
                elif prod[0] in self.terminals:
                    first.add(prod[0])
                else:
                    first.update(self.compute_first(prod[0]))

                for terminal in first - {'ε'}:
                    self.parsing_table[nt][terminal] = f'{nt} -> {" ".join(prod)}'

                if 'ε' in first:
                    for terminal in self.follow_sets[nt]:
                        self.parsing_table[nt][terminal] = f'{nt} -> ε'

    def print_parsing_table(self):
        print("\n=== LL(1) Parsing Table ===\n")
        terminals = list(self.terminals) + ['$']
        print("NT\t" + "\t".join(terminals))
        for nt in self.non_terminals:
            row = [nt]
            for t in terminals:
                row.append(self.parsing_table[nt].get(t, ""))
            print("\t".join(row))
        print("\n")
    def print(self):
        # List of terminals + '$'
        terminals = list(self.terminals) + ['$']
        
        # Create a 2D dictionary (row: non-terminals, col: terminals)
        table_dict = {}
        for nt in self.non_terminals:
            table_dict[nt] = {}
            for t in terminals:
                entry = self.parsing_table[nt].get(t, '')
                table_dict[nt][t] = entry

        # Convert to DataFrame
        df = pd.DataFrame(table_dict).T  # Transpose to get NTs as rows
        df.index.name = 'Non-Terminal'
        print("\n=== LL(1) Parsing Table (Structured) ===\n")
        print(df.fillna('').to_string())


# --------------------------
# ✅ Grammar Example
grammar = {
    'E': [['T', "E'"]],
    "E'": [['+', 'T', "E'"], ['ε']],
    'T': [['F', "T'"]],
    "T'": [['*', 'F', "T'"], ['ε']],
    'F': [['(', 'E', ')'], ['id']]
}

terminals = {'+', '*', '(', ')', 'id'}

# --------------------------
# ✅ Driver Code
parser = LL1Parser(grammar, terminals)
parser.construct_parse_table()
parser.print_parsing_table()
parser.print()
