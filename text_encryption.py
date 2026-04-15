# pip3 install pycryptodome for AES encryption,
# padding, SHA256, and MAC verification

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256, HMAC

# Generates Public Key
def generate_public_key(private_key, g, p):
    return pow(g, private_key, p)

# Generates Shared Key
def generate_shared_key(other_user_public_key, private_key, p):
    return pow(other_user_public_key, private_key, p)

# Derives AES key from shared key
def derive_key(shared_key):
    h = SHA256.new()
    h.update(str(shared_key).encode())
    return h.digest()  # 32 bytes (AES-256)

# Encrypt text with AES + HMAC
def encrypt_text(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    C = cipher.iv + ciphertext

    # HMAC
    h = HMAC.new(key, C, digestmod=SHA256)
    mac = h.digest()

    # Final hash
    H = SHA256.new(mac).digest()

    return C, H

# Decrypt text with verification
def decrypt_text(C, H, key):
    iv = C[:16]
    ciphertext = C[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    message = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

    # Recompute HMAC
    h = HMAC.new(key, C, digestmod=SHA256)
    mac = h.digest()
    computed_H = SHA256.new(mac).digest()

    if computed_H == H:
        return message
    else:
        return None