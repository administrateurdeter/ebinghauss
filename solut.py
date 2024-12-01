import itertools
import operator
import math

chiffres = [1, 4, 2, 11, 20, 22]
operations = [
    operator.add,
    operator.sub,
    operator.mul,
    operator.truediv,
]

def evaluer_expression(ops, ch):
    resultat = ch[0]
    for i, op in enumerate(ops):
        try:
            temp = op(resultat, ch[i + 1])
        except OverflowError:
            return float('inf')
        resultat = temp
    return resultat

def combinaisons_chiffres(chiffres):
    if len(chiffres) == 1:
        return [(chiffres[0],)]
    combinaisons = []
    for i in range(len(chiffres)):
        for j in range(i + 1, len(chiffres) + 1):
            nb = int(''.join(map(str, chiffres[i:j])))
            reste_chiffres = chiffres[:i] + chiffres[j:]
            for ch_comb in combinaisons_chiffres(reste_chiffres):
                combinaisons.append((nb,) + ch_comb)
    return combinaisons

meilleure_difference = float('inf')
meilleure_combinaison = None
meilleures_operations = None

for chiffres_comb in set(combinaisons_chiffres(chiffres)):
    for ops_perm in itertools.product(operations, repeat=len(chiffres_comb) - 1):
        try:
            resultat = evaluer_expression(ops_perm, chiffres_comb)
            difference = abs(resultat - 666)
            if difference < meilleure_difference:
                meilleure_difference = difference
                meilleure_combinaison = chiffres_comb
                meilleures_operations = ops_perm
        except (ZeroDivisionError, ValueError):
            continue

if meilleures_operations:
    print("Solution la plus proche trouvée:")
    print("Résultat :", evaluer_expression(meilleures_operations, meilleure_combinaison))
    print("Chiffres :", meilleure_combinaison)
    print("Opérations :", [op.__name__ for op in meilleures_operations])
else:
    print("Aucune solution trouvée")
