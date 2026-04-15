import random
import socket
import threading
import struct
import time
# from plyer import notification
from text_encryption import (
    encrypt_text, decrypt_text,
    derive_key, generate_public_key, generate_shared_key
)
from image_encryption import encrypt_image, decrypt_image
from PIL import Image
from io import BytesIO

SHARED_KEY = None

# --- Helper Functions ---

def send_dh(sock, p, g, public_key):
    data = f"{p},{g},{public_key}".encode()
    header = struct.pack("!4sQ", b"DHKE", len(data))
    sock.sendall(header + data)

def recv_exact(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

# --- Receive Thread ---

def receive_data(sock):
    while True:
        try:
            header = recv_exact(sock, 12)
            if not header:
                break

            msg_type, length = struct.unpack("!4sQ", header)
            msg_type = msg_type.decode()

            data = recv_exact(sock, length)
            if not data:
                break

            if msg_type == "TEXT":
                payload = data[:-32]
                recv_hash = data[-32:]

                message = decrypt_text(payload, recv_hash, SHARED_KEY)
                if message:
                    print(f"\n[Server]: {message}")

                print("Your Message: ", end='', flush=True)

            elif msg_type == "IMAGE":
                payload = data[:-32]
                recv_hash = data[-32:]

                image = decrypt_image(payload, recv_hash, SHARED_KEY)
                if image:
                    image.show()
                    print("\n[Server sent an image]")

                print("Your Message: ", end='', flush=True)

        except:
            break

    print("\nDisconnected from server.")
    sock.close()

# --- Send Functions ---

def send_text(sock, message):
    payload, h = encrypt_text(message, SHARED_KEY)
    data = payload + h

    header = struct.pack("!4sQ", b"TEXT", len(data))
    sock.sendall(header + data)

def send_image(sock, path):
    try:
        image = Image.open(path)
        payload, h = encrypt_image(image, SHARED_KEY)
        data = payload + h

        header = struct.pack("!4sQ", b"IMAGE", len(data))
        sock.sendall(header + data)

    except Exception as e:
        print(f"Failed to send image: {e}")

        

def send_data(sock):
    while True:
        try:
            message = input("Your Message: ")

            if message.startswith("/sendimage "):
                path = message[len("/sendimage "):].strip()
                send_image(sock, path)

            elif message.startswith("/sendtext "):
                send_text(sock, message[len("/sendtext "):].strip())

            elif message == "/quit":
                print("Disconnecting...")
                sock.close()
                break

            else:
                print("Commands:")
                print("  /sendtext <message>")
                print("  /sendimage <path>")
                print("  /quit")

        except Exception as e:
            print(f"Error: {e}")
            break

# --- Main Client ---

def client_script():
    host = input("Enter the IP ADDRESS: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, 8080))

    print(f"Connected to {host}:8080")
    print("Performing key exchange...")

    # Diffie-Hellman parameters
    p = 13240666412895696007
    g = 5
    private_key = random.randint(2**100, 2**200)

    public_key = generate_public_key(private_key, g, p)

    # Send DH
    send_dh(client_socket, p, g, public_key)

    # Receive server public key
    header = recv_exact(client_socket, 12)
    msg_type, length = struct.unpack("!4sQ", header)

    data = recv_exact(client_socket, length)
    server_public = int(data.decode())

    shared = generate_shared_key(server_public, private_key, p)

    global SHARED_KEY
    SHARED_KEY = derive_key(shared)

    print("Secure connection established.")

    # Threads
    threading.Thread(target=receive_data, args=(client_socket,), daemon=True).start()
    threading.Thread(target=send_data, args=(client_socket,), daemon=True).start()

    while True:
        time.sleep(1)

# --- Run ---

if __name__ == '__main__':
    client_script()