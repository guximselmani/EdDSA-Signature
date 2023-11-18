# EdDSA-Signature
QR Code Signature Generation using Edwards-curve Digital Signature algorithm

Duhet të instalohen bibliotekat e kërkuara për të ekzekutuar kodin me sukses:
```
import random
import hashlib
import qrcode
```

# Definimi
Në matematikë lakorja e Edwardit është pjesë e lakoreve eliptike
Ekuacioni i lakorës së Edwardit mbi një fushë K është x^2 + y^2 = 1 + dx^2*y^2
```
p = pow(2, 255) - 19
a = -1
d = -121665/121666
d = (-121665 * pow(121666, -1, p)) % p
```

```p - prime moduli```
```p = pow(2, 255) - 19``` është moduli kryesor. Është një numër i madh i thjeshtë që përcakton madhësinë e fushës së fundme mbi të cilën përcaktohet lakorja e Edwardit. Zgjedhja e këtij primi specifik është krijuar për të ofruar një nivel të lartë sigurie.
a, d - koeficienta qe definojne lakoren

Koeficienti a: është koeficienti në ekuacionin e lakorës së Edwardit. Zgjedhja specifike a=−1 thjeshton ekuacionin e lakorës. Është një zgjedhje e zakonshme për kriptografinë e lakorës eliptike pasi thjeshton disa llogaritje.

Koeficienti d: 
```d = -121665/121666 dhe d = (-121665 * pow(121666, -1, p)) % p``` është koeficienti në ekuacionin e lakores së  Edwardit që lidhet me formën e përdredhur të Edwardit. Llogaritja që përfshin d është bërë për të siguruar që ajo plotëson ekuacionin e përdredhur të kurbës Edwards.
Vlerat specifike për d janë pjesë e parametrave standardë për Ed25519. Zgjedhja e këtyre vlerave bazohet në sigurimin e veçorive të caktuara të sigurisë dhe llogaritjeve efikase.

Këto vlera janë të standardizuara dhe të dokumentuara si pjesë e sistemit të kriptografisë së kurbës eliptike Ed25519. Zgjedhjet specifike të parametrave bëhen për të balancuar sigurinë, efikasitetin dhe lehtësinë e zbatimit. Ato janë përzgjedhur me kujdes për të ofruar një nivel të lartë sigurie duke lejuar operacione aritmetike efikase në kurbën eliptike. Është e rëndësishme të theksohet se algoritmet kriptografike mbështeten në zgjedhje specifike të parametrave për të arritur garancitë e tyre të sigurisë dhe devijimet nga parametrat standard mund të rrezikojnë sigurinë.

Në përmbledhje, të dyja shprehjet llogaritin të njëjtën vlerë për d, por shprehja e dytë është një mënyrë numerikisht më e qëndrueshme dhe efikase për të kryer llogaritjen brenda kontekstit të aritmetikës modulare dhe fushave të fundme.

# Gjenerimi i qelsit
```
private_key = random.getrandbits(256)
public_key = apply_double_and_add_method(G, private_key, a, d, p)
```
G - pikë në lakore
apply_double_and_add_method - metodë që performon shumëzimin skalar te lakorës
add_points - metodë që shton pikat në lakore

# Gjenerimi i nënshkrimit
```
message = text_to_int("Hi it is done")
r = hashing(hashing(message) + message) % p
R = apply_double_and_add_method(G, r, a, d, p)
h = (R[0] + public_key[0] + message) % p
s = (r + h + private_key)
```

Nënshkrimi përbëhët prej palëve (R,s) ku R është një pikë në lakore dhe s është një skalarë

# Verifikimi i nënshkrimit
```
h = (R[0] + public_key[0] + message) % p
P1 = apply_double_and_add_method(G, s, a, d, p)
P2 = add_points(R, apply_double_and_add_method(public_key, h, a, d, p), a, d, p)
assert P1[0] == P2[0] and P1[1] == P2[1]
```

Bëhet krahasimi i dy pikave në lakore, duke vertetësuar validitetin e nënshkrimit

# Gjenerimi i QR CODE
Kjo mund të jetë e dobishme për ndarjen e të dhënave të nënshkrimit në një mënyrë të përshtatshme.
