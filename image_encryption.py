from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256
from Crypto.Hash import HMAC
import io

def encrypt_image(image, key):

    # Converting image to bytes for encryption.
    image_byte_arr = io.BytesIO()
    image.save(image_byte_arr, format=image.format)
    image_bytes = image_byte_arr.getvalue()

    # AES encryption of image.
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_bytes = cipher.encrypt(pad(image_bytes, AES.block_size))
    payload = cipher.iv + cipher_bytes

    # HMAC
    hmac = HMAC.new(key, payload, digestmod=SHA256).digest()
    
    # Hash
    hash = SHA256.new(hmac).digest()

    return(payload, hash)



def decrypt_image(payload, hash, key):

    # AES decryption of image.
    cipher_bytes = payload[16:]
    iv = payload[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    image_bytes = unpad(cipher.decrypt(cipher_bytes), AES.block_size)

    # Converting bytes to image.
    image = Image.open(io.BytesIO(image_bytes))

    # Verifying image.
    hmac = HMAC.new(key, payload, digestmod=SHA256).digest()
    verifying_hash = SHA256.new(hmac).digest()

    if hash == verifying_hash:
        return(image)
    else:
        print("Image Not Verified")
        return None
    




