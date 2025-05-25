from collections import defaultdict, deque

# Step 1: Grammar
productions = {
    "S": [["C", "C"]],
    "C": [["c", "C"], ["d"]]
}

# Augment grammar
def augment_grammar(productions):
    start = list(productions.keys())[0]
    new_productions = {"S'": [[start]]}
    new_productions.update(productions)
    return new_productions, "S'"

productions, start_symbol = augment_grammar(productions)

# Step 2: FIRST and FOLLOW sets
def compute_first(productions):
    first = defaultdict(set)

    def first_of(symbol):
        if symbol not in productions:
            return {symbol}
        if symbol in first and first[symbol]:
            return first[symbol]
        for prod in productions[symbol]:
            for sym in prod:
                first[symbol] |= first_of(sym)
                if "ε" not in first_of(sym):
                    break
        return first[symbol]

    for nt in productions:
        first_of(nt)
    return first

def compute_follow(productions, start_symbol, first):
    follow = defaultdict(set)
    follow[start_symbol].add("$")

    while True:
        updated = False
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                for i, symbol in enumerate(rhs):
                    if symbol in productions:
                        follow_set = set()
                        for sym in rhs[i+1:]:
                            follow_set |= (first[sym] - {"ε"})
                            if "ε" not in first[sym]:
                                break
                        else:
                            follow_set |= follow[lhs]
                        if not follow_set.issubset(follow[symbol]):
                            follow[symbol] |= follow_set
                            updated = True
        if not updated:
            break
    return follow

# Step 3: Closure and GOTO (for LR(0) items)
def closure(items, productions):
    closure_set = items[:]
    added = True
    while added:
        added = False
        new_items = []
        for lhs, rhs, dot in closure_set:
            if dot < len(rhs) and rhs[dot] in productions:
                B = rhs[dot]
                for prod in productions[B]:
                    item = (B, tuple(prod), 0)
                    if item not in closure_set and item not in new_items:
                        new_items.append(item)
                        added = True
        closure_set.extend(new_items)
    return closure_set

def goto(items, symbol, productions):
    moved = []
    for lhs, rhs, dot in items:
        if dot < len(rhs) and rhs[dot] == symbol:
            moved.append((lhs, tuple(rhs), dot+1))
    return closure(moved, productions)

# Step 4: Canonical collection of LR(0) items
def canonical_collection(productions):
    start_item = (start_symbol, tuple(productions[start_symbol][0]), 0)
    C = [closure([start_item], productions)]
    states = [C[0]]
    transitions = {}

    while True:
        new_states = []
        symbols = set(sym for prods in productions.values() for rhs in prods for sym in rhs)
        for i, state in enumerate(states):
            for sym in symbols:
                next_state = goto(state, sym, productions)
                if next_state and next_state not in states and next_state not in new_states:
                    new_states.append(next_state)
                    transitions[(i, sym)] = len(states) + len(new_states) - 1
                elif next_state:
                    existing_index = states.index(next_state) if next_state in states else states.index(next_state)
                    transitions[(i, sym)] = existing_index
        if not new_states:
            break
        states.extend(new_states)
    return states, transitions

# Step 5: Build ACTION and GOTO tables
def build_parsing_table(states, transitions, productions, follow):
    action = defaultdict(dict)
    goto_table = defaultdict(dict)

    state_map = {tuple(state): i for i, state in enumerate(states)}
    for i, state in enumerate(states):
        for item in state:
            lhs, rhs, dot = item
            if dot < len(rhs):
                symbol = rhs[dot]
                if symbol not in productions:
                    j = transitions.get((i, symbol))
                    if j is not None:
                        action[i][symbol] = f"s{j}"
                else:
                    j = transitions.get((i, symbol))
                    if j is not None:
                        goto_table[i][symbol] = j
            elif lhs != start_symbol:
                for terminal in follow[lhs]:
                    action[i][terminal] = f"r{lhs}->{' '.join(rhs)}"
            elif lhs == start_symbol:
                action[i]["$"] = "accept"
    return action, goto_table

# Step 6: Print everything
def print_table(action, goto):
    print("ACTION TABLE:")
    for state in sorted(action.keys()):
        print(f"State {state}: ", action[state])
    print("\nGOTO TABLE:")
    for state in sorted(goto.keys()):
        print(f"State {state}: ", goto[state])

# Execution
first = compute_first(productions)
follow = compute_follow(productions, start_symbol, first)
states, transitions = canonical_collection(productions)
action_table, goto_table = build_parsing_table(states, transitions, productions, follow)

print_table(action_table, goto_table)
