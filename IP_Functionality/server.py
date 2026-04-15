import random
import socket
import threading
import struct
# from plyer import notification
from text_encryption import (
    encrypt_text, decrypt_text,
    derive_key, generate_public_key, generate_shared_key
)
from image_encryption import encrypt_image, decrypt_image

clients = []  # list of (conn, shared_key)

# --- Helper Functions ---

def recv_exact(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

# --- Client Handler ---

def handle_client(conn, addr):
    print(f"Client {addr} connected.")

    try:
        # --- DH HANDSHAKE ---
        header = recv_exact(conn, 12)
        if not header:
            conn.close()
            return

        msg_type, length = struct.unpack("!4sQ", header)
        data = recv_exact(conn, length)

        p, g, client_public = map(int, data.decode().split(','))

        private_key = random.randint(2**100, 2**200)
        public_key = generate_public_key(private_key, g, p)

        # Send server public key
        response = str(public_key).encode()
        header = struct.pack("!4sQ", b"DHKE", len(response))
        conn.sendall(header + response)

        shared = generate_shared_key(client_public, private_key, p)
        shared_key = derive_key(shared)

        print(f"Secure channel established with {addr}")

        clients.append((conn, shared_key))

        # --- Messaging Loop ---
        while True:
            header = recv_exact(conn, 12)
            if not header:
                break

            msg_type, length = struct.unpack("!4sQ", header)
            msg_type = msg_type.decode()

            data = recv_exact(conn, length)
            if not data:
                break

            if msg_type == "TEXT":
                payload = data[:-32]
                recv_hash = data[-32:]

                message = decrypt_text(payload, recv_hash, shared_key)
                if message:
                    print(f"\n[{addr}]: {message}")
                    broadcast(conn, "TEXT", message)

            elif msg_type == "IMAGE":
                payload = data[:-32]
                recv_hash = data[-32:]

                image = decrypt_image(payload, recv_hash, shared_key)
                if image:
                    image.show()
                    print(f"\n[{addr}] sent an image")
                    broadcast(conn, "IMAGE", data, is_raw=True)

    except:
        pass

    # Cleanup
    for c in clients:
        if c[0] == conn:
            clients.remove(c)
            break

    conn.close()
    print(f"Client {addr} disconnected.")

# --- Broadcast ---

def broadcast(sender, msg_type, content, is_raw=False):
    for client, key in clients:
        if client != sender:
            try:
                if msg_type == "TEXT":
                    # Re-encrypt message per client
                    payload, h = encrypt_text(content, key)
                    new_data = payload + h

                elif msg_type == "IMAGE" and is_raw:
                    # Already encrypted, just forward
                    new_data = content

                else:
                    continue

                header = struct.pack("!4sQ", msg_type.encode(), len(new_data))
                client.sendall(header + new_data)

            except:
                pass

# --- Server Setup ---

def server_script():
    host = input("Enter the IP ADDRESS: ")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, 8080))
    server_socket.listen(5)

    print(f"Server running on {host}:8080")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# --- Run ---

if __name__ == "__main__":
    server_script()