# Found these based on research of Python libraries. May/May Not Use all of them.
import socket
import threading
import struct
from plyer import notification
from text_encryption import encrypt_message, decrypt_message, derive_key, generate_public_key, generate_shared_key
from image_encryption import encrypt_image, decrypt_image
from PIL import Image

# Import external scripts here:
# Example: import other_script

clients = []

def handle_client(conn, addr):
  print(f"Client {addr} connected.")

  # --- DH HANDSHAKE ---
  header = recv_exact(conn, 12)
  msg_type, length = struct.unpack("!4sQ", header)

  data = recv_exact(conn, length)
  p, g, client_public = map(int, data.decode().split(','))

  private_key = random.randint(1, 100)
  public_key = generate_public_key(private_key, g, p)

  # Send B
  response = str(public_key).encode()
  header = struct.pack("!4sQ", b"DHKE", len(response))
  conn.sendall(header + response)

  shared = generate_shared_key(client_public, private_key, p)
  shared_key = derive_key(shared)

  print(f"Secure channel established with {addr}")
  
  clients.append(conn)

  while True:
    try:
      header = conn.recv(12)
      if not header:
        break

      msg_type, length = struct.unpack("!4sQ", header)
      msg_type = msg_type.decode()

      data = b''
      while len(data) < length:
        packet = conn.recv(4096)
        if not packet:
          break
        data += packet

      if msg_type == "TEXT":
        payload = data[:-32]
        recv_hash = data[-32:]

        message = decrypt_message(payload, recv_hash, SHARED_KEY)
        if message:
          print(f"\n[{addr}]: {message}")
          print("Your Message: ", end='', flush=True)
          notification.notify(title=f"New Message from {addr}", message={message}, app_name="PythoChat", timeout=10)
          broadcast(conn, "TEXT", data)

        elif msg_type == "IMAGE":
          payload = data[:-32]
          recv_hash = data[-32:]

          image = decrypt_image(payload, recv_hash, SHARED_KEY)
          if image:
            image.show()
            print(f"\n[{addr} sent an image]")
            print("Your Message: ", end='', flush=True)
            notification.notify(title=f"New Image from {addr}", message="You received a new image.", app_name="PythoChat", timeout=10)
            broadcast(conn, "IMAGE", data)
    except:
      break

  clients.remove(conn)
  conn.close()
  print(f"Client {addr} disconnected.")

def broadcast(sender, msg_type, data):
    for client, key in clients:
      if client != sender:
          try:
              if msg_type == "TEXT":
                  payload = data[:-32]
                  h = data[-32:]
                  message = decrypt_text(payload, h, key)

                  new_payload, new_h = encrypt_text(message, key)
                  new_data = new_payload + new_h

              else:
                  # images already encrypted; forward directly
                  new_data = data

                header = struct.pack("!4sQ", msg_type.encode(), len(new_data))
                client.sendall(header + new_data)

          except:
              pass

# Host value is IP of the user's input.
# May use port value as a randomly-generated value above 1024 and at most 65000.
def server_script():
  host = input("Enter the IP ADDRESS value: ")
  port = input("Enter the PORT value: ")

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen(5)

  print(f"Server started on {host}:{port}. Waiting for connections...")

  while True:
    conn, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
  server_script()
