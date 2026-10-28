import unicodedata
import random
from collections import Counter


# TP5 — Corrigés de Christophe Guyeux — CC BY-NC-SA 4.0
# https://cours.gclab.fr/outils-fondamentaux/tp5-synthese/


# Exercice 1.1 : les deux conversions
def lettre_vers_nombre(c):
    """Numéro de 0 à 25 d'une lettre majuscule."""
    return ord(c) - ord("A")

def nombre_vers_lettre(n):
    """Lettre majuscule correspondant à un numéro de 0 à 25."""
    return chr(n % 26 + ord("A"))

print(lettre_vers_nombre("C"), nombre_vers_lettre(2))
print([nombre_vers_lettre(lettre_vers_nombre(c)) == c for c in "ABCXYZ"])


# Exercice 1.2 : nettoyer un texte
def nettoyer(texte):
    """Majuscules sans accents, lettres A-Z uniquement."""
    sans_accent = unicodedata.normalize("NFD", texte)
    sans_accent = "".join(c for c in sans_accent if unicodedata.category(c) != "Mn")
    return "".join(c for c in sans_accent.upper() if "A" <= c <= "Z")

print(nettoyer("Été, à Paris !"))


# Exercice 2.1 : la fonction de chiffrement
def chiffrer(texte, a, b):
    """Chiffrement affine de texte avec la clé (a, b)."""
    resultat = []
    for c in nettoyer(texte):
        x = lettre_vers_nombre(c)
        resultat.append(nombre_vers_lettre((a * x + b) % 26))
    return "".join(resultat)

message = "ATTAQUEALAUBE"
print(chiffrer(message, 5, 8))
print(chiffrer(message, 1, 3))   # le chiffre de César


# Exercice 3.1 : les clés utilisables
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

valides = [a for a in range(1, 26) if pgcd(a, 26) == 1]
print(valides)
print(len(valides), "valeurs possibles pour a")


# Exercice 3.2 : l'inverse modulaire
def inverse_modulaire(a, n):
    """Inverse de a modulo n, par recherche exhaustive."""
    a = a % n
    for candidat in range(1, n):
        if (a * candidat) % n == 1:
            return candidat
    raise ValueError(f"{a} n'est pas inversible modulo {n}")

print(inverse_modulaire(5, 26))
print((5 * 21) % 26)

try:
    inverse_modulaire(4, 26)
except ValueError as erreur:
    print("erreur attendue :", erreur)


# Exercice 4.1 : la fonction de déchiffrement
def dechiffrer(texte, a, b):
    """Déchiffrement affine. Lève une erreur si la clé n'est pas inversible."""
    a_inverse = inverse_modulaire(a, 26)
    resultat = []
    for c in nettoyer(texte):
        y = lettre_vers_nombre(c)
        resultat.append(nombre_vers_lettre(a_inverse * (y - b) % 26))
    return "".join(resultat)

message = nettoyer("Attaque a l aube")
secret = chiffrer(message, 5, 8)
print(secret)
print(dechiffrer(secret, 5, 8))
print(dechiffrer(secret, 5, 8) == message)

# une clé invalide est refusée au lieu de produire un résultat faux
try:
    dechiffrer(secret, 4, 7)
except ValueError as erreur:
    print("cle refusee :", erreur)


# Exercice 5.1 : essayer toutes les clés
def toutes_les_clefs(secret):
    """Tous les déchiffrements possibles, sous forme de triplets (a, b, texte)."""
    resultats = []
    for a in valides:
        for b in range(26):
            resultats.append((a, b, dechiffrer(secret, a, b)))
    return resultats

essais = toutes_les_clefs(secret)
print(len(essais), "clefs essayees")
bons = [e for e in essais if e[2] == message]
print("la bonne clef :", bons[0][0], bons[0][1])


# Exercice 6.1 : casser automatiquement
texte_long = nettoyer(
    "Le chiffrement affine est un chiffrement par substitution monoalphabetique. "
    "Chaque lettre du message est remplacee par une autre lettre, toujours la meme, "
    "ce qui laisse intactes les frequences relatives des lettres et permet de casser "
    "le code sans essayer toutes les clefs possibles."
)
secret_long = chiffrer(texte_long, 7, 12)

comptes = Counter(secret_long)
lettre_frequente = comptes.most_common(1)[0][0]
print("lettre la plus frequente du chiffre :", lettre_frequente)

# on suppose que E (numero 4) a ete chiffre en cette lettre
cible = lettre_vers_nombre(lettre_frequente)
candidats = []
for a in valides:
    # E -> cible impose b = cible - 4a mod 26
    b = (cible - 4 * a) % 26
    candidats.append((a, b, dechiffrer(secret_long, a, b)))

print(len(candidats), "candidats au lieu de 312")
for a, b, texte in candidats:
    if texte.startswith("LECHIFFREMENT"):
        print("trouve :", a, b)
        print(texte[:60])


# Exercice 7.1 : l'indice de coïncidence
def indice_coincidence(texte):
    """Probabilité que deux lettres tirées au hasard dans le texte coïncident."""
    N = len(texte)
    comptes = Counter(texte)
    return sum(n * (n - 1) for n in comptes.values()) / (N * (N - 1))

random.seed(1)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
hasard = "".join(random.choice(alphabet) for _ in range(len(texte_long)))

print(f"clair    : {indice_coincidence(texte_long):.4f}")
print(f"affine   : {indice_coincidence(secret_long):.4f}")
print(f"hasard   : {indice_coincidence(hasard):.4f}")


# Exercice 8.1 : chiffrer par Vigenère
def vigenere(texte, cle):
    """Chiffre de Vigenère : chaque lettre est décalée par la lettre de la clé en face."""
    resultat = []
    for i, c in enumerate(nettoyer(texte)):
        decalage = lettre_vers_nombre(cle[i % len(cle)])
        resultat.append(nombre_vers_lettre(lettre_vers_nombre(c) + decalage))
    return "".join(resultat)

secret_vigenere = vigenere(texte_long, "CLE")
print(secret_vigenere[:40])
print(f"IC vigenere : {indice_coincidence(secret_vigenere):.4f}")


# Exercice 8.2 : retrouver la longueur de la clé
for L in range(1, 8):
    colonnes = [secret_vigenere[i::L] for i in range(L)]
    moyenne = sum(indice_coincidence(col) for col in colonnes) / L
    print(f"L = {L} : indice moyen {moyenne:.4f}")
