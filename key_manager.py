#!/usr/bin/env python3
"""
Module de gestion des clés ECC
Génération, sauvegarde et chargement des clés
"""

import random
import base64
from ecc_math import EllipticCurve, Point


def generate_keys(curve, base_point, key_size=1000):
    """
    Génère une paire de clés (privée, publique)
    
    Args:
        curve: Courbe elliptique
        base_point: Point de base P
        key_size: Plage aléatoire pour k (défaut: 1000)
    
    Returns:
        tuple: (k, Q) où k est la clé privée et Q la clé publique
    """
    # Génère k aléatoirement entre 1 et key_size
    # On évite les points à l'infini en régénérant si nécessaire
    max_attempts = 100
    for _ in range(max_attempts):
        k = random.randint(1, key_size)
        # Calcule Q = k × P
        Q = curve.scalar_multiply(base_point, k)
        # Vérifie que Q n'est pas le point à l'infini
        if not Q.is_infinity():
            return k, Q
    
    # Si après 100 tentatives on n'a pas trouvé, on prend k=1
    k = 1
    Q = curve.scalar_multiply(base_point, k)
    return k, Q


def save_keys(k, Q, filename="monECC"):
    """
    Sauvegarde les clés dans des fichiers .priv et .pub
    
    Args:
        k: Clé privée (entier)
        Q: Clé publique (Point)
        filename: Nom de base des fichiers (sans extension)
    """
    # Sauvegarde de la clé privée
    priv_filename = f"{filename}.priv"
    with open(priv_filename, 'w') as f:
        f.write("---begin monECC private key---\n")
        # Encode k en base64
        k_str = str(k)
        k_encoded = base64.b64encode(k_str.encode('utf-8')).decode('utf-8')
        f.write(f"{k_encoded}\n")
        f.write("---end monECC key---\n")
    
    # Sauvegarde de la clé publique
    pub_filename = f"{filename}.pub"
    with open(pub_filename, 'w') as f:
        f.write("---begin monECC public key---\n")
        # Encode Qx;Qy en base64
        if Q.is_infinity():
            raise ValueError("Impossible de sauvegarder un point à l'infini comme clé publique")
        Q_str = f"{Q.x};{Q.y}"
        Q_encoded = base64.b64encode(Q_str.encode('utf-8')).decode('utf-8')
        f.write(f"{Q_encoded}\n")
        f.write("---end monECC key---\n")


def load_private_key(filename):
    """
    Charge une clé privée depuis un fichier
    
    Args:
        filename: Nom du fichier de clé privée
    
    Returns:
        int: La clé privée k
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Vérifie le format
    if not lines[0].strip() == "---begin monECC private key---":
        raise ValueError(f"Format de clé privée invalide dans {filename}")
    
    # Décode la clé
    k_encoded = lines[1].strip()
    k_str = base64.b64decode(k_encoded).decode('utf-8')
    k = int(k_str)
    
    return k


def load_public_key(filename):
    """
    Charge une clé publique depuis un fichier
    
    Args:
        filename: Nom du fichier de clé publique
    
    Returns:
        Point: La clé publique Q
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Vérifie le format
    if not lines[0].strip() == "---begin monECC public key---":
        raise ValueError(f"Format de clé publique invalide dans {filename}")
    
    # Décode la clé
    Q_encoded = lines[1].strip()
    Q_str = base64.b64decode(Q_encoded).decode('utf-8')
    Qx, Qy = map(int, Q_str.split(';'))
    
    return Point(Qx, Qy)


# Tests unitaires
if __name__ == "__main__":
    print("=== Test Gestion des clés ===")
    
    # Paramètres
    from ecc_math import EllipticCurve, Point
    A = 35
    B = 3
    MODULO = 101
    BASE_POINT = Point(2, 9)
    
    curve = EllipticCurve(A, B, MODULO)
    
    # Génère des clés
    k, Q = generate_keys(curve, BASE_POINT, 1000)
    print(f"Clé générée: k={k}, Q={Q}")
    
    # Sauvegarde
    save_keys(k, Q, "test_key")
    print("Clés sauvegardées dans test_key.priv et test_key.pub")
    
    # Charge
    k_loaded = load_private_key("test_key.priv")
    Q_loaded = load_public_key("test_key.pub")
    print(f"Clé chargée: k={k_loaded}, Q={Q_loaded}")
    
    print(f"Clés identiques: k={k == k_loaded}, Q={Q == Q_loaded}")
    
    # Affiche le contenu des fichiers
    print("\n--- Contenu test_key.priv ---")
    with open("test_key.priv", 'r') as f:
        print(f.read())
    
    print("--- Contenu test_key.pub ---")
    with open("test_key.pub", 'r') as f:
        print(f.read())

