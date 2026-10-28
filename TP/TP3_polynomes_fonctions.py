import math
import time
import matplotlib.pyplot as plt


# TP3 — Corrigés de Christophe Guyeux — CC BY-NC-SA 4.0
# https://cours.gclab.fr/outils-fondamentaux/tp3-polynomes-fonctions/


# Exercice 1.1 : évaluation naïve
def evaluer_naif(P, x):
    """Évalue le polynôme P au point x, terme par terme."""
    total = 0
    for i in range(len(P)):
        total = total + P[i] * x ** i
    return total

print(evaluer_naif([2, 3, 0, 5], 2))
print(evaluer_naif([2, 3, 0, 5], 0))


# Exercice 2.1 : Horner
def evaluer(P, x):
    """Évalue le polynôme P au point x par le schéma de Horner."""
    total = 0
    for coefficient in reversed(P):
        total = total * x + coefficient
    return total

P = [2, 3, 0, 5]
for x in (-2, 0, 1, 2, 10):
    print(x, evaluer_naif(P, x), evaluer(P, x))


# Exercice 2.2 : mesurer, et se méfier de ses prévisions
for degre in (1000, 5000, 20000):
    P = [1] * (degre + 1)

    debut = time.perf_counter()
    a = evaluer_naif(P, 1.0001)
    t_naif = time.perf_counter() - debut

    debut = time.perf_counter()
    b = evaluer(P, 1.0001)
    t_horner = time.perf_counter() - debut

    print(f"degre {degre:>6} : naif {t_naif:.5f} s | horner {t_horner:.5f} s "
          f"| rapport {t_naif / t_horner:.1f} | ecart des valeurs {abs(a - b):.2e}")


# Exercice 2.3 : le cas où l'écart explose vraiment
for degre in (200, 400, 800):
    P = [1] * (degre + 1)

    debut = time.perf_counter()
    a = evaluer_naif(P, 3)
    t_naif = time.perf_counter() - debut

    debut = time.perf_counter()
    b = evaluer(P, 3)
    t_horner = time.perf_counter() - debut

    print(f"degre {degre:>4} : rapport {t_naif / t_horner:.1f} | resultats egaux : {a == b}")


# Exercice 3.1 : la dérivée
def deriver(P):
    """Coefficients du polynôme dérivé de P."""
    return [i * P[i] for i in range(1, len(P))]

print(deriver([2, 3, 0, 5]))
print(deriver([7]))


# Exercice 4.1 : dichotomie
def dichotomie(f, a, b, tolerance=1e-12):
    """Racine de f dans [a, b], par bissection. Exige f(a) et f(b) de signes opposés."""
    fa, fb = f(a), f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("f(a) et f(b) doivent etre de signes opposes")
    while b - a > tolerance:
        milieu = (a + b) / 2
        if f(a) * f(milieu) <= 0:
            b = milieu
        else:
            a = milieu
    return (a + b) / 2

def carre_moins_deux(x):
    return x * x - 2

racine = dichotomie(carre_moins_deux, 0, 2)
print(racine)
print(abs(racine - 2 ** 0.5) < 1e-9)


# Exercice 4.2 : Newton sur un polynôme
def newton(P, depart, tolerance=1e-12, tours_max=100):
    """Racine du polynôme P par la méthode de Newton, à partir de depart."""
    derivee = deriver(P)
    x = float(depart)
    for tour in range(tours_max):
        valeur = evaluer(P, x)
        pente = evaluer(derivee, x)
        if pente == 0:
            raise ZeroDivisionError("tangente horizontale, Newton ne peut pas continuer")
        suivant = x - valeur / pente
        if abs(suivant - x) <= tolerance * max(1.0, abs(suivant)):
            return suivant, tour + 1
        x = suivant
    raise RuntimeError("pas de convergence en {} tours".format(tours_max))

# x^3 - 2x - 5
Q = [-5, -2, 0, 1]
racine, tours = newton(Q, 2)
print(racine, "en", tours, "tours")
print(abs(evaluer(Q, racine)) < 1e-10)


# Exercice 4.3 : faire échouer Newton
def newton_trace(P, depart, tours):
    """Renvoie la liste des premiers itérés de Newton, sans test d'arrêt."""
    derivee = deriver(P)
    x = float(depart)
    trajet = [x]
    for _ in range(tours):
        pente = evaluer(derivee, x)
        if pente == 0:
            break
        x = x - evaluer(P, x) / pente
        trajet.append(x)
    return trajet

R = [2, -2, 0, 1]          # x^3 - 2x + 2
print(newton_trace(R, 0, 8))

try:
    print(newton(R, 0))
except RuntimeError as erreur:
    print("echec :", erreur)


# Exercice 4.4 : le prix d'un mauvais point de départ
Q = [-5, -2, 0, 1]
for depart in (2, 1, 0):
    racine, tours = newton(Q, depart)
    print(f"depart {depart:>2} : {tours:>2} tours, racine {racine:.9f}")


# Étape 5. Voir la fonction (15 min)
Q = [-5, -2, 0, 1]          # x^3 - 2x - 5
xs = [i / 100 for i in range(-300, 301)]
ys = [evaluer(Q, x) for x in xs]

plt.figure()
plt.plot(xs, ys, label="x^3 - 2x - 5")
plt.axhline(0, linewidth=0.8)
plt.axvline(0, linewidth=0.8)
plt.ylim(-20, 20)
plt.xlabel("x")
plt.ylabel("P(x)")
plt.legend()
plt.title("Un polynome et son unique racine reelle")
plt.show()


# Exercice 6.1 : somme et produit
def somme(P, Q):
    """Somme de deux polynômes donnés par leurs coefficients."""
    longueur = max(len(P), len(Q))
    P = P + [0] * (longueur - len(P))
    Q = Q + [0] * (longueur - len(Q))
    return [P[i] + Q[i] for i in range(longueur)]

def produit_poly(P, Q):
    """Produit de deux polynômes donnés par leurs coefficients."""
    if not P or not Q:
        return []
    R = [0] * (len(P) + len(Q) - 1)
    for i in range(len(P)):
        for j in range(len(Q)):
            R[i + j] = R[i + j] + P[i] * Q[j]
    return R

print(somme([1, 2], [0, 0, 3]))
print(produit_poly([1, 1], [1, 1]))
print(produit_poly([-1, 1], [1, 1]))


# Exercice 6.2 : le triangle de Pascal, par les polynômes
binome = [1]
for _ in range(10):
    binome = produit_poly(binome, [1, 1])
print(binome)
print(sum(binome), 2 ** 10)


# Exercice 7.1 : trouver le meilleur pas
def derivee_avant(f, x, h):
    return (f(x + h) - f(x)) / h

def derivee_centree(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

exacte = math.cos(1.0)
for h in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12):
    e_avant = abs(derivee_avant(math.sin, 1.0, h) - exacte)
    e_centree = abs(derivee_centree(math.sin, 1.0, h) - exacte)
    print(f"h = {h:.0e} : avant {e_avant:.1e} | centree {e_centree:.1e}")


# Exercice 8.1 : les trois méthodes
def rectangles(f, a, b, n):
    """Intégrale de f sur [a, b] par n rectangles à gauche."""
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))

def trapezes(f, a, b, n):
    """Intégrale de f sur [a, b] par n trapèzes."""
    h = (b - a) / n
    interieur = sum(f(a + i * h) for i in range(1, n))
    return h * ((f(a) + f(b)) / 2 + interieur)

def simpson(f, a, b, n):
    """Intégrale de f sur [a, b] par la méthode de Simpson, n pair."""
    if n % 2 == 1:
        n = n + 1
    h = (b - a) / n
    impairs = sum(f(a + i * h) for i in range(1, n, 2))
    pairs = sum(f(a + i * h) for i in range(2, n, 2))
    return h / 3 * (f(a) + f(b) + 4 * impairs + 2 * pairs)

def carre(x):
    return x * x

for n in (10, 100, 1000):
    e_rect = abs(rectangles(carre, 0, 1, n) - 1 / 3)
    e_trap = abs(trapezes(carre, 0, 1, n) - 1 / 3)
    e_simp = abs(simpson(carre, 0, 1, n) - 1 / 3)
    print(f"n = {n:>4} : rectangles {e_rect:.1e} | trapezes {e_trap:.1e} | simpson {e_simp:.1e}")


# Exercice 8.2 : calculer π
def arctangente_derivee(x):
    return 4 / (1 + x * x)

approx_trap = trapezes(arctangente_derivee, 0, 1, 1000)
approx_simp = simpson(arctangente_derivee, 0, 1, 1000)
print(approx_trap, abs(approx_trap - math.pi))
print(approx_simp, abs(approx_simp - math.pi))
