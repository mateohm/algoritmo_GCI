from collections import defaultdict

# Gramática ejemplo 
# E → T E'
# E' → + T E' | ε
# T → F T'
# T' → * F T' | ε
# F → ( E ) | id

grammar = {
    "E": [["T", "E'"]],
    "E'": [["+", "T", "E'"], ["ε"]],
    "T": [["F", "T'"]],
    "T'": [["*", "F", "T'"], ["ε"]],
    "F": [["(", "E", ")"], ["id"]]
}

non_terminals = list(grammar.keys())
terminals = set()

# Detectar todos los terminales
for prods in grammar.values():
    for prod in prods:
        for symbol in prod:
            if symbol not in grammar and symbol != 'ε':
                terminals.add(symbol)

# Algoritmo PRIMEROS
first = defaultdict(set)

def compute_first(symbol):
    if symbol in terminals:
        return {symbol}
    if symbol == "ε":
        return {"ε"}
    if symbol in first and first[symbol]:  # Ya calculado
        return first[symbol]

    result = set()
    for production in grammar[symbol]:
        for sym in production:
            sym_first = compute_first(sym)
            result.update(sym_first - {"ε"})
            if "ε" not in sym_first:
                break
        else:
            result.add("ε")
    first[symbol] = result
    return result

# Algoritmo SIGUIENTES
follow = defaultdict(set)
start_symbol = list(grammar.keys())[0]
follow[start_symbol].add("$")  # símbolo de fin de entrada

def compute_follow():
    changed = True
    while changed:
        changed = False
        for lhs in grammar:
            for production in grammar[lhs]:
                for i, B in enumerate(production):
                    if B in grammar:  # solo no terminales
                        trailer = set(follow[B])
                        # analizar lo que sigue después de B
                        for j in range(i + 1, len(production)):
                            beta = production[j]
                            first_beta = compute_first(beta)
                            follow[B].update(first_beta - {"ε"})
                            if "ε" in first_beta:
                                continue
                            break
                        else:
                            follow_before = set(follow[B])
                            follow[B].update(follow[lhs])
                            if follow[B] != follow_before:
                                changed = True

# Tabla de PREDICCIÓN
parse_table = defaultdict(dict)

def build_parse_table():
    for A in grammar:
        for production in grammar[A]:
            first_alpha = set()
            for symbol in production:
                first_alpha |= compute_first(symbol)
                if "ε" not in compute_first(symbol):
                    break
            else:
                first_alpha.add("ε")

            for terminal in (first_alpha - {"ε"}):
                parse_table[A][terminal] = production
            if "ε" in first_alpha:
                for terminal in follow[A]:
                    parse_table[A][terminal] = production

# Ejecutar todos los pasos
for non_terminal in grammar:
    compute_first(non_terminal)

compute_follow()
build_parse_table()

# Mostrar resultados
print("PRIMEROS:")
for nt in grammar:
    print(f"First({nt}) = {first[nt]}")

print("\nSIGUIENTES:")
for nt in grammar:
    print(f"Follow({nt}) = {follow[nt]}")

print("\nTABLA DE PREDICCIÓN:")
for nt in parse_table:
    for t in parse_table[nt]:
        print(f"M[{nt}, {t}] = {' '.join(parse_table[nt][t])}")
