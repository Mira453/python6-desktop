from typing import List, Tuple, Set

def parse_clause(clause: str) -> Set[str]:
    """Розбити диз'юнкт на множину літералів."""
    return set(clause.replace(" ", "").split("v"))

def resolve(clause1: Set[str], clause2: Set[str]) -> List[Set[str]]:
    """Застосувати резолюцію до двох диз'юнктів і повернути отримані результатні диз'юнкти."""
    результатні = []
    for літерал in clause1:
        if f"~{літерал}" in clause2 or (літерал.startswith("~") and літерал[1:] in clause2):
            контрарний = f"~{літерал}" if not літерал.startswith("~") else літерал[1:]
            новий_дизюнкт = (clause1 | clause2) - {літерал, контрарний}
            результатні.append(новий_дизюнкт)
    return результатні

def resolution(clauses: List[Set[str]], goal: Set[str]) -> bool:
    """Застосувати алгоритм резолюції для доведення мети."""
    clauses.append(set(f"~{літерал}" for літерал in goal))  # Додаємо заперечення мети
    нові = set()

    while True:
        пари = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
        for (clause1, clause2) in пари:
            print(f"Резолюція між: {clause1} та {clause2}")  
            результатні = resolve(clause1, clause2)
            for результатний in результатні:
                print(f"Отримано: {результатний}")  
                if not результатний:  # Знайдено порожній диз'юнкт
                    print("Знайдено порожній диз'юнкт! Мета доведена.")
                    return True
                нові.add(frozenset(результатний))

        if all(frozenset(c) in map(frozenset, clauses) for c in нові):
            print("Нових диз'юнктів немає. Мету не вдалося довести.")
            return False  

        clauses.extend(map(set, нові))

if __name__ == "__main__":
    knowledge_base = [
        parse_clause("~p v q"),
        parse_clause("~p v s"),
        parse_clause("s"),
    ]
    goal = parse_clause("p")  # Мета: p

    if resolution(knowledge_base, goal):
        print("Мета доведена.")
    else:
        print("Мету не вдалося довести.")