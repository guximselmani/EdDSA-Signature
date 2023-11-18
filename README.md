# EdDSA-Signature
QR Code Signature Generation using Edwards-curve Digital Signature algorithm

Duhet të instalohen bibliotekat e kërkuara për të ekzekutuar kodin me sukses:
import random
import hashlib
import qrcode

# Definimi
Në matematikë lakorja e Edwardit është pjesë e lakoreve eliptike
Ekuacioni i lakorës së Edwardit mbi një fushë K është x^2 + y^2 = 1 + dx^2*y^2

p = pow(2, 255) - 19
a = -1
d = -121665/121666
d = (-121665 * pow(121666, -1, p)) % p

p - prime moduli
a, d - koeficienta qe definojne lakoren

# Gjenerimi i qelsit
private_key = random.getrandbits(256)
public_key = apply_double_and_add_method(G, private_key, a, d, p)

G - pikë në lakore
apply_double_and_add_method - metodë që performon shumëzimin skalar te lakorës
add_points - metodë që shton pikat në lakore

# Gjenerimi i nënshkrimit
message = text_to_int("Hi it is done")
r = hashing(hashing(message) + message) % p
R = apply_double_and_add_method(G, r, a, d, p)
h = (R[0] + public_key[0] + message) % p
s = (r + h + private_key)

Nënshkrimi përbëhët prej palëve (R,s) ku R është një pikë në lakore dhe s është një skalarë

# Verifikimi i nënshkrimit
h = (R[0] + public_key[0] + message) % p
P1 = apply_double_and_add_method(G, s, a, d, p)
P2 = add_points(R, apply_double_and_add_method(public_key, h, a, d, p), a, d, p)
assert P1[0] == P2[0] and P1[1] == P2[1]

Bëhet krahasimi i dy pikave në lakore, duke vertetësuar validitetin e nënshkrimit

# Gjenerimi i QR CODE
Kjo mund të jetë e dobishme për ndarjen e të dhënave të nënshkrimit në një mënyrë të përshtatshme.
