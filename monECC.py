#!/usr/bin/env python3
"""
MonECC - Implementation ECC
Auteur: Mamadou BARRY
Courbe: Y² = X³ + 35X + 3 (modulo 101)
Point de depart: P(2, 9)
"""

import sys
import base64
import hashlib
from ecc_math import EllipticCurve, Point
from crypto_utils import hash_secret, aes_encrypt, aes_decrypt
from key_manager import generate_keys, save_keys, load_public_key, load_private_key

#parametre
A = 35
B = 3
MODULO = 101 
BASE_POINT = Point(2, 9)


def print_help():
    print("""
Script monECC par Mamadou BARRY

Syntaxe:
    monECC <commande> [<clé>] [<texte>] [switchs]

Commande:
    keygen  : Génère une paire de clés
    crypt   : Chiffre <texte> pour la clé publique <clé>
    decrypt : Déchiffre <texte> pour la clé privée <clé>
    help    : Affiche ce manuel

Clé:
    Un fichier qui contient une clé publique monECC ("crypt") ou 
    une clé privée ("decrypt")

Texte:
    Une phrase en clair ("crypt") ou une phrase chiffrée ("decrypt")

Switchs:
    -f <file>  : Permet de choisir le nom des clés générées
                 (monECC.pub et monECC.priv par défaut)
    -s <size>  : Plage d'aléa pour la génération de clé (défaut: 1000)
    -i         : Lire depuis un fichier texte
    -o <file>  : Écrire dans un fichier de sortie

Exemples:
    python monECC.py keygen
    python monECC.py keygen -f alice
    python monECC.py crypt bob.pub "Hello Bob!"
    python monECC.py decrypt alice.priv "texte_chiffré"
""")


def cmd_keygen(args):
    filename = "monECC"
    key_size = 1000
    
    i = 0
    while i < len(args):
        if args[i] == "-f" and i + 1 < len(args):
            filename = args[i + 1]
            i += 2
        elif args[i] == "-s" and i + 1 < len(args):
            key_size = int(args[i + 1])
            i += 2
        else:
            i += 1
    
    curve = EllipticCurve(A, B, MODULO)
    k, Q = generate_keys(curve, BASE_POINT, key_size)
    save_keys(k, Q, filename)
    
    print(f"Cles generees avec succes!")
    print(f"  - Cle privee: {filename}.priv")
    print(f"  - Cle publique: {filename}.pub")
    print(f"  - k (prive) = {k}")
    print(f"  - Q (public) = ({Q.x}, {Q.y})")


def cmd_crypt(args):
    if len(args) < 2:
        print("Erreur: paramètres manquants")
        print("Usage: monECC crypt <clé_publique> <texte>")
        sys.exit(1)
    
    public_key_file = args[0]
    message = args[1]
    output_file = None
    use_input_file = False
    
    i = 2
    while i < len(args):
        if args[i] == "-o" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] == "-i":
            use_input_file = True
            i += 1
        else:
            i += 1
    
    if use_input_file:
        try:
            with open(message, 'r', encoding='utf-8') as f:
                message = f.read()
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier: {e}")
            sys.exit(1)
    
    try:
        Qb = load_public_key(public_key_file)
    except Exception as e:
        print(f"Erreur lors du chargement de la cle publique: {e}")
        sys.exit(1)
    
    curve = EllipticCurve(A, B, MODULO)
    k_ephemeral, Q_ephemeral = generate_keys(curve, BASE_POINT, 1000)
    S = curve.scalar_multiply(Qb, k_ephemeral)
    secret_hash = hash_secret(S)
    ciphertext = aes_encrypt(message, secret_hash)
    header = f"{Q_ephemeral.x};{Q_ephemeral.y}:"
    result = base64.b64encode(header.encode('utf-8') + ciphertext).decode('utf-8')
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Message chiffre ecrit dans: {output_file}")
    else:
        print(f"Texte chiffré:")
        print(result)


def cmd_decrypt(args):
    if len(args) < 2:
        print("Erreur: paramètres manquants")
        print("Usage: monECC decrypt <clé_privée> <texte_chiffré>")
        sys.exit(1)
    
    private_key_file = args[0]
    ciphertext = args[1]
    output_file = None
    use_input_file = False
    
    i = 2
    while i < len(args):
        if args[i] == "-o" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] == "-i":
            use_input_file = True
            i += 1
        else:
            i += 1
    
    if use_input_file:
        try:
            with open(ciphertext, 'r', encoding='utf-8') as f:
                ciphertext = f.read().strip()
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier: {e}")
            sys.exit(1)
    
    try:
        k = load_private_key(private_key_file)
    except Exception as e:
        print(f"Erreur lors du chargement de la cle privee: {e}")
        sys.exit(1)
    
    try:
        decoded = base64.b64decode(ciphertext)
        separator = decoded.find(b':')
        if separator == -1:
            raise ValueError("Format de message invalide")
        
        ephemeral_coords = decoded[:separator].decode('utf-8')
        encrypted_data = decoded[separator+1:]
        Qx, Qy = map(int, ephemeral_coords.split(';'))
        Q_ephemeral = Point(Qx, Qy)
    except Exception as e:
        print(f"Erreur lors du decodage: {e}")
        sys.exit(1)
    
    curve = EllipticCurve(A, B, MODULO)
    S = curve.scalar_multiply(Q_ephemeral, k)
    secret_hash = hash_secret(S)
    
    try:
        plaintext = aes_decrypt(encrypted_data, secret_hash)
    except Exception as e:
        print(f"Erreur lors du dechiffrement: {e}")
        sys.exit(1)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plaintext)
        print(f"Message dechiffre ecrit dans: {output_file}")
    else:
        print(f"Texte en clair:")
        print(plaintext)


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
    
    command = sys.argv[1].lower()
    args = sys.argv[2:]
    
    if command == "help":
        print_help()
    elif command == "keygen":
        cmd_keygen(args)
    elif command == "crypt":
        cmd_crypt(args)
    elif command == "decrypt":
        cmd_decrypt(args)
    else:
        print(f"Erreur: commande inconnue '{command}'")
        print("Utilisez 'help' pour voir les commandes disponibles")
        sys.exit(1)


if __name__ == "__main__":
    main()

