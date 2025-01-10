def occurs_check(var, term, subst):

    if var == term:
        return True
    elif isinstance(term, tuple):
        return any(occurs_check(var, t, subst) for t in term)
    elif term in subst:
        return occurs_check(var, subst[term], subst)
    return False

def unify_var(var, value, subst):

    if var in subst:
        return unify(subst[var], value, subst)
    elif value in subst:
        return unify(var, subst[value], subst)
    elif occurs_check(var, value, subst):
        return None
    else:
        subst[var] = value
        return subst

def unify(term1, term2, subst=None):

    if subst is None:
        subst = {}
    if term1 == term2:
        return subst
    elif isinstance(term1, str) and term1.islower():
        return unify_var(term1, term2, subst)
    elif isinstance(term2, str) and term2.islower():
        return unify_var(term2, term1, subst)
    elif isinstance(term1, tuple) and isinstance(term2, tuple):
        if len(term1) != len(term2):
            return None
        for t1, t2 in zip(term1, term2):
            subst = unify(t1, t2, subst)
            if subst is None:
                return None
        return subst
    return None

# Приклад із таблиці 2
term1 = ("P", "a", "f(g(y))")
term2 = ("P", "z", "f(n)")

unifier = unify(term1, term2)
if unifier:
    print("Уніфікатор:", unifier)
else:
    print("Уніфікація неможлива")