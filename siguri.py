import random
import hashlib
import qrcode

def add_points(P, Q, a, d, p):
    x1, y1 = P
    x2, y2 = Q
    
    x3 = ( ( (x1*y2 + y1*x2) % p) * pow(1 + d*x1*x2*y1*y2, -1, p) ) % p
    y3 = ( ( (y1*y2 - a*x1*x2) % p) * pow(1 - d*x1*x2*y1*y2, -1, p) ) % p
    
    assert (a*x3*x3 + y3*y3) % p == (1 + d*x3*x3*y3*y3) % p
    
    return x3, y3

def apply_double_and_add_method(Q, k, a, d, p):
    addition_point = Q
    
    k_binary = bin(k)[2:] #1111111101
    
    for i in range(1, len(k_binary)):
        current_bit = k_binary[i:i+1]
        
        # always doubling
        addition_point = add_points(addition_point, addition_point, a, d, p)
        
        if current_bit == "1":
            addition_point = add_points(addition_point, Q, a, d, p)
    
    return addition_point

p = pow(2, 255) - 19
a = -1

d = -121665/121666
d = (-121665 * pow(121666, -1, p)) % p


# base point G
u = 9
# Gy = (u-1)/(u+1)
Gy = (u-1) * pow(u+1, -1, p) % p
Gx = 15112221349535400772501151409588531511454012693041857206046113283949847762202

G = (Gx, Gy)

assert (a*Gx*Gx + Gy*Gy) % p == (1 + d*Gx*Gx*Gy*Gy) % p

private_key = random.getrandbits(256)
public_key = apply_double_and_add_method(G, private_key, a, d, p)

# print(private_key)
# print(public_key)

# sign messsage
def text_to_int(text):
    encoded_text = text.encode("utf-8")
    hex_text = encoded_text.hex()
    return int(hex_text, 16)

def hashing(message_int):
    return int(hashlib.sha256(str(message_int).encode("utf-8")).hexdigest(), 16)

message = text_to_int("Hi it is done")
print(message)
r = hashing(hashing(message) + message) % p

R = apply_double_and_add_method(G, r, a, d, p)

h = (R[0] + public_key[0] + message) % p
s = (r + h + private_key)

# verify
# message, (R, s), public_key, a, d, p, G 

h = (R[0] + public_key[0] + message) % p

P1 = apply_double_and_add_method(G, s, a, d, p)
P2 = add_points(R, apply_double_and_add_method(public_key, h, a, d, p), a, d, p)

P1[0] == P2[0] and P1[1] == P2[1]

# print(P1)

# s = (r + h * private_key)
# P1 = sxG
# P1 = (r + h * private_key) x G 
# P1 = rxg + h * private_key* G 
# P1 = R + h * private_key


# Create a QR Code for the signature
signature_data = {
    "message": message,
    "R": R,
    "s": s,
    "public_key": public_key,
    "a": a,
    "d": d,
    "p": p,
    "G": G
}

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(str(signature_data))
qr.make(fit=True)

# Display or Save the QR Code
img = qr.make_image(fill_color="black", back_color="white")
img.save("signature_qr.png") 