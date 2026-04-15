# This file is very likely to change a lot, this is more of a basic idea of what we will need to implement.

import socket
import threading
import struct
import sys
from plyer import notification
from text_encryption import encrypt_text, decrypt_text, derive_key, generate_public_key, generate_shared_key
from image_encryption import encrypt_image, decrypt_image
from PIL import Image

# External scripts go here:
# Examples:
#   import other_script
#   import

def recieve_data(sock):
  # Acts like the server version, but instead receives data from the server.
  while True:
    try:
      header = sock.recv(12)
      if not header:
        break
      msg_type, length = struct.unpack("!4sQ", header)
      msg_type = msg_type.decode()
      data = b''
      while len(data) < length:
        packet = sock.recv(4096)
        if not packet:
          break
        data += packet

      if msg_type == "TEXT":
        payload = data[:-32]
        recv_hash = data[-32:]
        message = decrypt_text(payload, recv_hash, SHARED_KEY)
        print(f"\n[Server]: {message}")
        print("Your Message: ", end='', flush=True)
        notification.notify(title="New Message from Server", message={message}, app_name="PythoChat", timeout=10)
      elif msg_type == "IMAGE":
        payload = data[:-32]
        recv_hash = data[-32:]
        image = decrypt_image(payload, h, SHARED_KEY)

        image.show()
        print("\n[Server sent an image]")
        print("Your Message: ", end='', flush=True)

    except:
      break
  print("Server has disconnected")
  sock.close()

def send_text(sock, message):
  payload, hash = encrypt_text(message, SHARED_KEY)
  data = payload + hash
  header = struct.pack("!4sQ", b"TEXT", len(data))
  sock.sendall(header + data)

def send_image(sock, path):
  try:
    image = Image.open(path)
    payload, hash = encrypt_image(image, SHARED_KEY)
    data = payload + hash

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
        send_image(sock)
      elif message.startswith("/sendtext "):
        send_text(sock)
      elif message == "/quit":
        print("Disconnecting from server...")
        sock.close()
        break
      else:
        print("Invalid command. Use /sendtext <message> or /sendimage <path> or /quit.")
    except Exception as e:
      print(f"Error sending data: {e}")
      break

def client_script():
  host = input("Enter the IP ADDRESS value: ")
  port = input("Enter the PORT value: ")
  
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((host, port))
  print(f"\nConnected to {host}:{port}")

  print(" Performing key exchange...")

  # DH parameters (simple version)
  p = 13240666412895696007
  g = 5
  private_key = random.randint(1, 100)

  public_key = generate_public_key(private_key, g, p)

  # Send (p, g, A)
  send_dh(sock, p, g, public_key)

  # Receive B
  header = recv_exact(sock, 12)
  msg_type, length = struct.unpack("!4sQ", header)
  data = recv_exact(sock, length)

  server_public = int(data.decode())

  shared = generate_shared_key(server_public, private_key, p)
  global SHARED_KEY
  SHARED_KEY = derive_key(shared)

  print("Secure connection established.")
  
  # Receive thread goes here. It will handle receiving data.
  threading.Thread(target=recieve_data, args=(client_socket,), daemon=True).start()
  # Send thread logic goes here. Will probably just be a while loop.
  threading.Thread(target=send_data, args=(client_socket,), daemon=True).start()

  while True:
    pass

if __name__ == '__main__':
  client_script()
