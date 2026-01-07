#!/usr/bin/env python3
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def hash_secret(secret_point):
    # hashlib est maintenant correctement importé
    secret_hash = hashlib.sha256(str(secret_point.x).encode()).digest()
    secret_hash = hashlib.sha256(secret_hash + str(secret_point.y).encode()).digest()
    return secret_hash


def aes_encrypt(plaintext, secret_hash):
    iv = secret_hash[:16]
    key = secret_hash[-16:]
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode('utf-8'))
    padded_data += padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return ciphertext


def aes_decrypt(ciphertext, secret_hash):
    iv = secret_hash[:16]
    key = secret_hash[-16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_data)
    plaintext += unpadder.finalize()
    
    return plaintext.decode('utf-8')


if __name__ == "__main__":
    print("=== Test AES ===")
    
    from ecc_math import Point
    
    # Crée un secret fictif
    secret = Point(123456, 654321)
    secret_hash = hash_secret(secret)
    
    print(f"Secret hash (hex): {secret_hash.hex()}")
    print(f"Longueur: {len(secret_hash)} octets")
    
    # Test chiffrement/déchiffrement
    texte = "Hello World! Ceci est un test de chiffrement AES."
    print(f"\nTexte original: {texte}")
    
    ciphertext = aes_encrypt(texte, secret_hash)
    print(f"Texte chiffré (hex): {ciphertext.hex()[:50]}...")
    print(f"Longueur: {len(ciphertext)} octets")
    
    plaintext = aes_decrypt(ciphertext, secret_hash)
    print(f"Texte déchiffré: {plaintext}")
    
    print(f"\nDéchiffrement réussi: {texte == plaintext}")

