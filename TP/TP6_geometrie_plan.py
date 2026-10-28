import math
import random
import matplotlib.pyplot as plt


# TP6 — Corrigés de Christophe Guyeux — CC BY-NC-SA 4.0
# https://cours.gclab.fr/outils-fondamentaux/tp6-geometrie-plan/


# Exercice 1.1 : la boîte à outils
def vecteur(A, B):
    """Vecteur AB, de A vers B."""
    return (B[0] - A[0], B[1] - A[1])

def produit_scalaire(u, v):
    return u[0] * v[0] + u[1] * v[1]

def norme(u):
    return math.hypot(u[0], u[1])

def angle(u, v):
    """Angle non orienté entre u et v, en degrés."""
    cosinus = produit_scalaire(u, v) / (norme(u) * norme(v))
    cosinus = max(-1.0, min(1.0, cosinus))
    return math.degrees(math.acos(cosinus))

print(norme((3, 4)), produit_scalaire((1, 2), (3, 4)))
print(angle((1, 0), (1, 1)), angle((1, 0), (0, 1)))
print(angle((2, 0), (2, 0)))


# Exercice 1.2 : la distance d'un point à une droite
def determinant(u, v):
    """Déterminant de (u, v), aire orientée du parallélogramme qu'ils engendrent."""
    return u[0] * v[1] - u[1] * v[0]

def distance_point_droite(P, A, B):
    AB = vecteur(A, B)
    AP = vecteur(A, P)
    return abs(determinant(AB, AP)) / norme(AB)

print(distance_point_droite((0, 0), (0, 1), (1, 0)), math.sqrt(2) / 2)
print(distance_point_droite((3, 4), (0, 0), (1, 0)))


# Exercice 2.1 : à gauche ou à droite ?
def orientation(A, B, C):
    """1 si A -> B -> C tourne à gauche, -1 à droite, 0 si alignés."""
    d = determinant(vecteur(A, B), vecteur(A, C))
    if d > 0:
        return 1
    if d < 0:
        return -1
    return 0

print(orientation((0, 0), (1, 0), (1, 1)))
print(orientation((0, 0), (1, 0), (1, -1)))
print(orientation((0, 0), (1, 1), (2, 2)))


# Exercice 2.2 : l'aire d'un polygone
def aire(polygone):
    """Aire d'un polygone simple donné par ses sommets dans l'ordre (formule du lacet)."""
    somme = 0
    n = len(polygone)
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]
        somme = somme + (x1 * y2 - x2 * y1)
    return abs(somme) / 2

carre = [(0, 0), (1, 0), (1, 1), (0, 1)]
triangle = [(0, 0), (4, 0), (0, 3)]
maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
print(aire(carre), aire(triangle), aire(maison))


# Exercice 3.1 : le test de croisement
def se_coupent(A, B, C, D):
    """Vrai si les segments [AB] et [CD] se croisent franchement.

    Les cas dégénérés (trois points alignés) renvoient False.
    """
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    return o1 * o2 < 0 and o3 * o4 < 0

print(se_coupent((0, 0), (1, 1), (0, 1), (1, 0)))
print(se_coupent((0, 0), (1, 0), (0, 1), (1, 1)))
print(se_coupent((0, 0), (1, 1), (2, 2), (3, 3)))


# Exercice 3.2 : le point d'intersection
def intersection(A, B, C, D):
    """Point d'intersection des segments [AB] et [CD], ou None."""
    AB = vecteur(A, B)
    CD = vecteur(C, D)
    denominateur = determinant(AB, CD)
    if denominateur == 0:
        return None            # parallèles ou alignés
    AC = vecteur(A, C)
    t = determinant(AC, CD) / denominateur
    u = determinant(AC, AB) / denominateur
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (A[0] + t * AB[0], A[1] + t * AB[1])
    return None

print(intersection((0, 0), (2, 2), (0, 2), (2, 0)))
print(intersection((0, 0), (1, 0), (0, 1), (1, 1)))
print(intersection((0, 0), (1, 1), (2, 2), (3, 3)))


# Exercice 4.1 : le lancer de rayon
def dedans(P, polygone):
    """Vrai si P est à l'intérieur du polygone, par lancer de rayon horizontal."""
    x, y = P
    n = len(polygone)
    interieur = False
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            x_croisement = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_croisement:
                interieur = not interieur
    return interieur

for P in ((1, 1), (1, 2.4), (3, 1), (0.2, 2.2)):
    print(P, dedans(P, maison))


# Exercice 4.2 : l'aire par le hasard
random.seed(0)
tirages = 200_000
touches = 0
for _ in range(tirages):
    P = (random.uniform(0, 2), random.uniform(0, 2.5))
    if dedans(P, maison):
        touches = touches + 1

aire_rectangle = 2 * 2.5
print(aire_rectangle * touches / tirages)


# Étape 5. Dessiner (20 min)
def tracer_polygone(polygone, points=()):
    xs = [s[0] for s in polygone] + [polygone[0][0]]
    ys = [s[1] for s in polygone] + [polygone[0][1]]
    plt.figure(figsize=(5, 5))
    plt.plot(xs, ys, color="black")
    for P in points:
        couleur = "green" if dedans(P, polygone) else "red"
        plt.scatter([P[0]], [P[1]], color=couleur)
    plt.axis("equal")
    plt.title("Vert : dedans, rouge : dehors")
    plt.show()

random.seed(1)
nuage = [(random.uniform(-0.5, 2.5), random.uniform(-0.5, 3)) for _ in range(60)]
tracer_polygone(maison, nuage)


# Exercice 5.1 : un polygone qui n'est pas convexe
etoile = []
for k in range(10):
    rayon = 2 if k % 2 == 0 else 0.8
    theta = math.pi / 2 + k * math.pi / 5
    etoile.append((rayon * math.cos(theta), rayon * math.sin(theta)))

print(round(aire(etoile), 4))
print(dedans((0, 0), etoile), dedans((0, 1.5), etoile), dedans((1.2, 1.2), etoile))
tracer_polygone(etoile, [(0, 0), (0, 1.5), (1.2, 1.2), (0, 1.9)])


# Exercice 6.1 : le polygone le plus proche
def zone_de(P, zones):
    """Indice de la première zone qui contient P, ou None."""
    for indice, zone in enumerate(zones):
        if dedans(P, zone):
            return indice
    return None

zones = [maison, [(3, 0), (4, 0), (4, 1), (3, 1)]]
for P in ((1, 1), (3.5, 0.5), (2.5, 0.5)):
    print(P, zone_de(P, zones))
