# Guide de test MonECC

## Installation

```bash
python3 -m pip install -r requirements.txt
```

## Test 1: Modules individuels

```bash
python3 ecc_math.py
python3 key_manager.py
python3 crypto_utils.py
```

Verifier que chaque test affiche "True" ou "reussi" a la fin.

## Test 2: Generation de cles

```bash
python3 monECC.py keygen
```

Verifier que les fichiers monECC.priv et monECC.pub sont crees.

```bash
python3 monECC.py keygen -f alice
python3 monECC.py keygen -f bob
```

Verifier que alice.priv, alice.pub, bob.priv, bob.pub sont crees.

## Test 3: Chiffrement et dechiffrement

```bash
python3 monECC.py crypt bob.pub "Message test" -o message.txt
python3 monECC.py decrypt bob.priv message.txt -i
```

Le message dechiffre doit etre "Message test".

## Test 4: Echange entre deux utilisateurs

```bash
python3 monECC.py crypt bob.pub 'Salut Bob!' -o msg_alice.txt
python3 monECC.py decrypt bob.priv msg_alice.txt -i
```

Bob doit voir "Salut Bob!".

```bash
python3 monECC.py crypt alice.pub 'Salut Alice!' -o msg_bob.txt
python3 monECC.py decrypt alice.priv msg_bob.txt -i
```

Alice doit voir "Salut Alice!".

## Test 5: Fichiers texte

```bash
echo "Message dans un fichier" > test.txt
python3 monECC.py crypt bob.pub test.txt -i -o encrypted.txt
python3 monECC.py decrypt bob.priv encrypted.txt -i
```

## Test 6: Caracteres speciaux

```bash
python3 monECC.py crypt bob.pub 'Accents: éàü, symboles: @#\$%!' -o special.txt
python3 monECC.py decrypt bob.priv special.txt -i
```

## Test 7: Message long

```bash
python3 monECC.py crypt bob.pub 'Ceci est un tres long message pour tester le padding et le chiffrement de textes de taille variable.' -o long.txt
python3 monECC.py decrypt bob.priv long.txt -i
```

## Test 8: Verification format des cles

```bash
cat alice.priv
```

Doit afficher:
```
---begin monECC private key---
[base64]
---end monECC key---
```

```bash
cat alice.pub
```

Doit afficher:
```
---begin monECC public key---
[base64]
---end monECC key---
```

## Test 9: Securite

```bash
python3 monECC.py crypt bob.pub 'Secret' -o secret.txt
python3 monECC.py decrypt alice.priv secret.txt -i
```

Alice ne doit pas pouvoir dechiffrer le message de Bob. Doit afficher une erreur ou du charabia.

## Nettoyage

```bash
rm -f *.priv *.pub *.txt test.txt
```

