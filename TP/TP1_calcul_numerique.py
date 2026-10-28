import math
import sys
from fractions import Fraction


# Exercice 1.1 : division euclidienne
n = 2026
d = 7
quotient = n // d
reste = n % d
print(quotient, reste)
print(quotient * d + reste == n)


# Exercice 1.2 : dernier chiffre
n = 123456789
print(n % 10)
print(n // 10)


# Exercice 2.1 : l'erreur qui s'accumule
total = 0.0
for _ in range(1000):
    total = total + 0.1
print(total)
print(total - 100)


# Exercice 2.2 : la fonction de comparaison
def presque_egaux(a, b, tolerance=1e-9):
    """Dit si a et b sont égaux à la tolérance près."""
    return abs(a - b) <= tolerance

print(presque_egaux(0.1 + 0.2, 0.3))
print(presque_egaux(1.0, 1.5))


# Exercice 3.1 : la table de sept
for i in range(1, 11):
    print(7, "x", i, "=", 7 * i)


# Exercice 3.2 : une somme et sa formule
n = 100
total = 0
for i in range(1, n + 1):
    total = total + i
print(total)
print(n * (n + 1) // 2)


# Exercice 4.1 : compter les chiffres
def nombre_de_chiffres(n):
    """Renvoie le nombre de chiffres de l'entier positif n."""
    compte = 1
    while n >= 10:
        n = n // 10
        compte = compte + 1
    return compte

print(nombre_de_chiffres(2026))
print(nombre_de_chiffres(7))
print(nombre_de_chiffres(10 ** 60))


# Exercice 5.1 : racine carrée de 2
def heron(a, tolerance=1e-12):
    """Racine carrée de a par la méthode de Héron."""
    if a < 0:
        raise ValueError("pas de racine carrée réelle pour un nombre négatif")
    if a == 0:
        return 0.0
    x = float(a)
    tours = 0
    while True:
        suivant = 0.5 * (x + a / x)
        tours = tours + 1
        if abs(suivant - x) <= tolerance * abs(suivant):
            return suivant
        x = suivant

print(heron(2))
print(math.sqrt(2))
print(abs(heron(2) - math.sqrt(2)) < 1e-12)


# Exercice 6.1 : conversion en binaire, à la main
def vers_binaire(n):
    """Écriture binaire de l'entier positif n, sans le préfixe 0b."""
    if n == 0:
        return "0"
    chiffres = ""
    while n > 0:
        chiffres = str(n % 2) + chiffres
        n = n // 2
    return chiffres

print(vers_binaire(37), vers_binaire(0), vers_binaire(1024))
print(all(vers_binaire(n) == bin(n)[2:] for n in range(2000)))


# Exercice 6.2 : l'epsilon de la machine
eps = 1.0
while 1.0 + eps / 2 != 1.0:
    eps = eps / 2

print(eps)
print(sys.float_info.epsilon)
print(eps == 2 ** -52)


# Exercice 7.1 : la formule du lycée en difficulté
def racines_naif(a, b, c):
    """Racines réelles de ax² + bx + c par la formule classique."""
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("pas de racine réelle")
    r = math.sqrt(delta)
    return (-b - r) / (2 * a), (-b + r) / (2 * a)

petite, grande = racines_naif(1.0, -1e8, 1.0)
print(petite, grande)
print("produit :", petite * grande, "attendu : 1")


# Exercice 7.2 : la formule stable
def racines(a, b, c):
    """Racines réelles de ax² + bx + c, sans élimination catastrophique."""
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("pas de racine réelle")
    r = math.sqrt(delta)
    # on choisit le signe qui additionne au lieu de soustraire
    if b >= 0:
        sure = (-b - r) / (2 * a)
    else:
        sure = (-b + r) / (2 * a)
    autre = c / (a * sure)
    return min(sure, autre), max(sure, autre)

petite, grande = racines(1.0, -1e8, 1.0)
print(petite, grande)
print("produit :", petite * grande)
for x in (petite, grande):
    residu = x * x - 1e8 * x + 1
    print(f"residu : {residu:.1e}, soit {residu / max(x * x, 1.0):.1e} en relatif")


# Exercice 7.3 : calculer exactement, quand c'est possible
total = Fraction(0)
for _ in range(1000):
    total = total + Fraction(1, 10)
print(total, total == 100)
print(Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))
