from typing import Tuple, Union, List

# Представлення термів
class Term:
    def __init__(self, name: str, args: List['Term'] = None):
        self.name = name
        self.args = args if args else []

    def is_variable(self):
        return self.name.islower() and not self.args

    def __repr__(self):
        if self.args:
            return f"{self.name}({', '.join(map(str, self.args))})"
        return self.name

# Уніфікація
class Unification:
    @staticmethod
    def unify(term1: Term, term2: Term, substitution: dict = None) -> Union[dict, None]:
        if substitution is None:
            substitution = {}

        if term1 == term2:
            return substitution

        if term1.is_variable():
            return Unification._unify_variable(term1, term2, substitution)

        if term2.is_variable():
            return Unification._unify_variable(term2, term1, substitution)

        if term1.name != term2.name or len(term1.args) != len(term2.args):
            return None

        for arg1, arg2 in zip(term1.args, term2.args):
            substitution = Unification.unify(arg1, arg2, substitution)
            if substitution is None:
                return None

        return substitution

    @staticmethod
    def _unify_variable(var: Term, term: Term, substitution: dict) -> Union[dict, None]:
        if var.name in substitution:
            return Unification.unify(substitution[var.name], term, substitution)

        if term.name in substitution:
            return Unification.unify(var, substitution[term.name], substitution)

        if Unification._occurs_check(var, term, substitution):
            return None

        substitution[var.name] = term
        return substitution

    @staticmethod
    def _occurs_check(var: Term, term: Term, substitution: dict) -> bool:
        if var == term:
            return True

        if term.is_variable() and term.name in substitution:
            return Unification._occurs_check(var, substitution[term.name], substitution)

        if term.args:
            return any(Unification._occurs_check(var, arg, substitution) for arg in term.args)

        return False

# Тестовий приклад
if __name__ == "__main__":
    # Приклад: P(a, x, f(g(v))) та P(z, f(z), f(n))
    pred1 = Term("P", [
        Term("a"),
        Term("x"),
        Term("f", [Term("g", [Term("v")])])
    ])

    pred2 = Term("P", [
        Term("z"),
        Term("f", [Term("z")]),
        Term("f", [Term("n")])
    ])

    substitution = Unification.unify(pred1, pred2)

    if substitution:
        print("Уніфікатор:", substitution)
        print("Результуючий предикат:", pred1)
    else:
        print("Уніфікація неможлива.")

