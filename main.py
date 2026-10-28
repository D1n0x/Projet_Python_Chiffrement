# Projet : chiffrer et reconstruire un dessin
# Chiffrement affine, comme au TP5, avec un modulo adapté.
# Préparation assistée par ChatGPT : vérifications et commentaires .
# Bibliothèque nécessaire pour les graphiques : matplotlib.

import math
import matplotlib.pyplot as plt


# TP3 : construire un toit courbe avec un polynôme et Horner

def evaluer(P, x):
    resultat = 0
    for coefficient in reversed(P):
        resultat = resultat * x + coefficient
    return resultat


def creer_dessin(nombre_segments):
    if nombre_segments < 2:
        raise ValueError("Il faut au moins deux segments pour le toit.")
    # Toit : y = 3 + x - 0.25*x², pour x compris entre 0 et 4.
    P = [3, 1, -0.25]
    points = [(0, 0), (4, 0)]
    for i in range(nombre_segments + 1):
        x = 4 - 4 * i / nombre_segments
        points.append((x, evaluer(P, x)))
    return points


# TP4 : produit matriciel, rotation et translation en coordonnées homogènes

def produit(A, B):
    n, p = len(A), len(A[0])
    if len(B) != p:
        raise ValueError("Dimensions incompatibles.")
    q = len(B[0])
    C = [[0] * q for _ in range(n)]
    for i in range(n):
        for j in range(q):
            for k in range(p):
                C[i][j] = C[i][j] + A[i][k] * B[k][j]
    return C


def transformer(points, angle, tx, ty):
    c, s = math.cos(angle), math.sin(angle)
    R = [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    T = [[1, 0, tx], [0, 1, ty], [0, 0, 1]]
    M = produit(T, R)  # Rotation d'abord, puis translation.
    resultat = []
    for x, y in points:
        image = produit(M, [[x], [y], [1]])
        resultat.append((image[0][0], image[1][0]))
    return resultat


# TP6 : aire d'un polygone, formule du lacet

def aire(points):
    somme = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        somme = somme + x1 * y2 - x2 * y1
    return abs(somme) / 2


# TP1 : convertir les coordonnées en entiers et mesurer les arrondis

def encoder(points, precision, borne):
    # Les coordonnées doivent être dans [-borne, borne].
    # Le décalage permet de représenter aussi les coordonnées négatives.
    if precision <= 0 or borne <= 0:
        raise ValueError("La précision et la borne doivent être positives.")
    nombres = []
    for x, y in points:
        for valeur in (x, y):
            if abs(valeur) > borne:
                raise ValueError("Une coordonnée dépasse la borne choisie.")
            nombres.append(round(valeur * precision) + borne * precision)
    return nombres


def decoder(nombres, precision, borne):
    if len(nombres) % 2 != 0:
        raise ValueError("Il faut deux nombres par point.")
    points = []
    for i in range(0, len(nombres), 2):
        x = (nombres[i] - borne * precision) / precision
        y = (nombres[i + 1] - borne * precision) / precision
        points.append((x, y))
    return points


def erreur_maximale(original, copie):
    erreur = 0
    for i in range(len(original)):
        for j in range(2):
            erreur = max(erreur, abs(original[i][j] - copie[i][j]))
    return erreur


# TP2 : PGCD pour vérifier la clé

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# TP5 : inverse modulaire et chiffrement affine

def inverse_modulaire(a, modulo):
    for candidat in range(1, modulo):
        if a * candidat % modulo == 1:
            return candidat
    raise ValueError("La clé n'est pas inversible.")


def chiffrer(nombres, a, b, modulo):
    if modulo < 2 or pgcd(a, modulo) != 1:
        raise ValueError("La clé a doit être première avec le modulo.")
    resultat = []
    for nombre in nombres:
        if not 0 <= nombre < modulo:
            raise ValueError("Nombre hors de l'intervalle du chiffrement.")
        resultat.append((a * nombre + b) % modulo)
    return resultat


def dechiffrer(nombres, a, b, modulo):
    if modulo < 2 or pgcd(a, modulo) != 1:
        raise ValueError("La clé a doit être première avec le modulo.")
    inverse = inverse_modulaire(a, modulo)
    return [inverse * (nombre - b) % modulo for nombre in nombres]


# TP3 et TP6 : afficher des points reliés avec matplotlib

def tracer(points, titre):
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]
    plt.figure()
    plt.plot(xs, ys, "o-")
    plt.axis("equal")
    plt.title(titre)
    plt.xlabel("x")
    plt.ylabel("y")


if __name__ == "__main__":
    print("CHIFFREMENT AFFINE D'UN DESSIN")

    # 1. Création et transformation du dessin.
    dessin = creer_dessin(20)
    transforme = transformer(dessin, math.pi / 6, 2, 1)
    print("Nombre de points :", len(dessin))
    print("Aire avant transformation :", aire(dessin))
    print("Aire après transformation :", aire(transforme))
    print("Aire conservée :", math.isclose(aire(dessin), aire(transforme)))

    # 2. Encodage au centième et chiffrement.
    precision = 100
    borne = 100
    modulo = 2 * borne * precision + 1
    a, b = 7, 123
    nombres = encoder(transforme, precision, borne)
    secret = chiffrer(nombres, a, b, modulo)
    retrouves = dechiffrer(secret, a, b, modulo)
    reconstruit = decoder(retrouves, precision, borne)

    print("Premières coordonnées encodées :", nombres[:8])
    print("Premiers nombres chiffrés :", secret[:8])
    print("Entiers retrouvés exactement :", retrouves == nombres)
    print("Erreur maximale sur les coordonnées :",
          erreur_maximale(transforme, reconstruit))
    print("Écart d'aire après reconstruction :",
          abs(aire(transforme) - aire(reconstruit)))

    # 3. Comparaison des précisions : l'erreur vient de l'arrondi avant chiffrement.
    print("\nPRÉCISION DES COORDONNÉES")
    for precision_test in (10, 100, 1000):
        modulo_test = 2 * borne * precision_test + 1
        valeurs = encoder(transforme, precision_test, borne)
        chiffres = chiffrer(valeurs, a, b, modulo_test)
        clairs = dechiffrer(chiffres, a, b, modulo_test)
        copie = decoder(clairs, precision_test, borne)
        erreur = erreur_maximale(transforme, copie)
        print("Précision :", precision_test,
              "| erreur :", round(erreur, 8),
              "| entiers identiques :", clairs == valeurs)

    # 4. Le toit est une suite de segments : sa surface dépend de leur nombre.
    print("\nNOMBRE DE SEGMENTS DU TOIT")
    for segments in (4, 10, 20, 100):
        print(segments, "segments | aire :", aire(creer_dessin(segments)))

    # 5. Vérification du refus d'une clé invalide.
    try:
        chiffrer(nombres, 3, b, modulo)  # 20001 est divisible par 3.
    except ValueError as erreur:
        print("\nClé invalide refusée :", erreur)

    # Limite : deux nombres identiques donnent le même résultat chiffré.
    print("Répétitions visibles :", chiffrer([100, 100], a, b, modulo))
    print("Ce chiffrement pédagogique n'est pas adapté à des données sensibles.")

    # 6. Trois vues : original, coordonnées chiffrées, dessin reconstruit.
    # Relier les nombres chiffrés ne leur donne aucune signification géométrique.
    tracer(transforme, "Dessin avant chiffrement")
    tracer(decoder(secret, precision, borne), "Coordonnées chiffrées")
    tracer(reconstruit, "Dessin après déchiffrement")
    plt.show()
