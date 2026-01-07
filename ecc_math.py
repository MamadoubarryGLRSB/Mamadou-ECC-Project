#!/usr/bin/env python3
"""
Module de mathématiques pour courbes elliptiques
Implémentation complète des opérations ECC (fait main)
"""


class Point:
    """Représente un point sur une courbe elliptique"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def is_infinity(self):
        """Vérifie si le point est le point à l'infini"""
        return self.x is None and self.y is None


class EllipticCurve:
    """Représente une courbe elliptique y² = x³ + ax + b (mod p)"""
    
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
    
    def is_on_curve(self, point):
        """Vérifie si un point est sur la courbe"""
        if point.is_infinity():
            return True
        left = (point.y * point.y) % self.p
        right = (point.x * point.x * point.x + self.a * point.x + self.b) % self.p
        return left == right
    
    def mod_inverse(self, a):
        """Calcule l'inverse modulaire de a modulo p (algorithme d'Euclide étendu)"""
        if a < 0:
            a = a % self.p
        # Algorithme d'Euclide étendu
        old_r, r = a, self.p
        old_s, s = 1, 0
        
        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
        
        if old_r > 1:
            raise ValueError(f"{a} n'a pas d'inverse modulo {self.p}")
        
        return old_s % self.p
    
    def add(self, P, Q):
        """Additionne deux points P et Q sur la courbe"""
        # Point à l'infini
        if P.is_infinity():
            return Q
        if Q.is_infinity():
            return P
        
        # Cas P = -Q (même x, y opposé)
        if P.x == Q.x:
            if P.y == (-Q.y) % self.p or (P.y + Q.y) % self.p == 0:
                return Point(None, None)  # Point à l'infini
            else:
                # P = Q, on fait le doublement
                return self.double(P)
        
        # Calcul de la pente
        delta_x = (Q.x - P.x) % self.p
        delta_y = (Q.y - P.y) % self.p
        
        # Inverse de delta_x
        inv_delta_x = self.mod_inverse(delta_x)
        slope = (delta_y * inv_delta_x) % self.p
        
        # Calcul du nouveau point
        x3 = (slope * slope - P.x - Q.x) % self.p
        y3 = (slope * (P.x - x3) - P.y) % self.p
        
        return Point(x3, y3)
    
    def double(self, P):
        """Double un point P (P + P = 2P)"""
        if P.is_infinity():
            return P
        
        if P.y == 0:
            return Point(None, None)  # Point à l'infini
        
        # Pente de la tangente: (3x² + a) / (2y)
        numerator = (3 * P.x * P.x + self.a) % self.p
        denominator = (2 * P.y) % self.p
        inv_denominator = self.mod_inverse(denominator)
        slope = (numerator * inv_denominator) % self.p
        
        # Calcul du nouveau point
        x3 = (slope * slope - 2 * P.x) % self.p
        y3 = (slope * (P.x - x3) - P.y) % self.p
        
        return Point(x3, y3)
    
    def scalar_multiply(self, P, k):
        """Calcule k × P en utilisant l'algorithme Double-and-Add"""
        if k == 0:
            return Point(None, None)  # Point à l'infini
        
        if k == 1:
            return P
        
        # Algorithme Double-and-Add
        result = Point(None, None)  # Point à l'infini
        addend = P
        
        # Traiter k bit par bit
        while k > 0:
            if k & 1:  # Si le bit est 1
                if result.is_infinity():
                    result = addend
                else:
                    result = self.add(result, addend)
            
            # Doubler pour le prochain bit
            addend = self.double(addend)
            k >>= 1  # Décalage à droite
        
        return result


# Tests unitaires
if __name__ == "__main__":
    print("=== Tests ECC ===")
    
    # Paramètres de la courbe
    A = 35
    B = 3
    MODULO = 101
    BASE_POINT = Point(2, 9)
    
    curve = EllipticCurve(A, B, MODULO)
    
    print(f"Courbe: y² = x³ + {A}x + {B} (mod {MODULO})")
    print(f"Point de base P: {BASE_POINT}")
    print(f"P est sur la courbe: {curve.is_on_curve(BASE_POINT)}")
    
    # Test 2P
    P2 = curve.double(BASE_POINT)
    print(f"\n2P = {P2}")
    print(f"2P est sur la courbe: {curve.is_on_curve(P2)}")
    
    # Test 3P
    P3 = curve.add(BASE_POINT, P2)
    print(f"3P = {P3}")
    print(f"3P est sur la courbe: {curve.is_on_curve(P3)}")
    
    # Test 25P
    P25 = curve.scalar_multiply(BASE_POINT, 25)
    print(f"\n25P = {P25}")
    print(f"25P est sur la courbe: {curve.is_on_curve(P25)}")
    
    # Test échange de clés
    print("\n=== Test échange de clés ===")
    ka = 7
    kb = 13
    
    Qa = curve.scalar_multiply(BASE_POINT, ka)
    Qb = curve.scalar_multiply(BASE_POINT, kb)
    
    print(f"Alice: k={ka}, Q={Qa}")
    print(f"Bob: k={kb}, Q={Qb}")
    
    # Secret partagé
    Sa = curve.scalar_multiply(Qb, ka)  # Alice calcule ka × Qb
    Sb = curve.scalar_multiply(Qa, kb)  # Bob calcule kb × Qa
    
    print(f"Secret Alice: {Sa}")
    print(f"Secret Bob: {Sb}")
    print(f"Secrets égaux: {Sa == Sb}")

