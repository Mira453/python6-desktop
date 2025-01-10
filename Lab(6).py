from itertools import combinations

def resolve(clause1, clause2):
    for literal in clause1:
        if -literal in clause2:
            new_clause = (clause1 - {literal}) | (clause2 - {-literal})
            return new_clause
    return None

def resolution(clauses):
    new = set()
    while True:
        pairs = list(combinations(clauses, 2))
        for (clause1, clause2) in pairs:
            resolvent = resolve(clause1, clause2)
            if resolvent is not None:
                print(f"Резолюція: {clause1} та {clause2} => {resolvent}")
                if not resolvent:  
                    print("Знайдена суперечність.")
                    return True
                new.add(frozenset(resolvent))
        if new.issubset(clauses):  # Немає нових диз'юнктів
            return False
        clauses = clauses.union(new)

# Приклад із таблиці 1
clauses = {
    frozenset({-1, 2}),  # ¬p ∨ q
    frozenset({-2, 3}),  # ¬q ∨ r
    frozenset({-3}),     # ¬r
}
print("Виконуваність:", resolution(clauses))