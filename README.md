# MonECC - Systeme de chiffrement ECC

Auteur: Mamadou BARRY M2 AL

## Description

Implementation d'un systeme de chiffrement base sur les courbes elliptiques (ECC) en Python.

Parametres de la courbe:
- Equation: Y² = X³ + 35X + 3 (modulo 101)
- Point de base P: (2, 9)
- Algorithme de chiffrement: AES-CBC
- Fonction de hachage: SHA-256

## Installation

```bash
pip install -r requirements.txt
```

## Structure

```
monECC.py          Programme principal
ecc_math.py        Operations mathematiques ECC
key_manager.py     Gestion des cles
crypto_utils.py    Chiffrement AES
requirements.txt   Dependances
```

## Utilisation

### Generation de cles

```bash
python monECC.py keygen
python monECC.py keygen -f alice
python monECC.py keygen -s 5000
```

### Chiffrement

```bash
python monECC.py crypt destinataire.pub "Message"
python monECC.py crypt bob.pub message.txt -i
python monECC.py crypt bob.pub "Secret" -o encrypted.txt
```

### Dechiffrement

```bash
python monECC.py decrypt alice.priv "texte_chiffre"
python monECC.py decrypt alice.priv encrypted.txt -i
python monECC.py decrypt alice.priv encrypted.txt -i -o decrypted.txt
```

### Aide

```bash
python monECC.py help
```

## Exemple

```bash
python monECC.py keygen -f alice
python monECC.py keygen -f bob
python monECC.py crypt bob.pub "Salut Bob!" -o message.txt
python monECC.py decrypt bob.priv message.txt -i
```

## Format des fichiers de cles

Clé privée (.priv):
```
---begin monECC private key---
[base64]
---end monECC key---
```

Clé publique (.pub):
```
---begin monECC public key---
[base64]
---end monECC key---
```

Les valeurs sont encodees en Base64.
