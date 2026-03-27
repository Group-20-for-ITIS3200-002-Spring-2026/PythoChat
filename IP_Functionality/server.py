# Found these based on research of Python libraries. May/May Not Use all of them.
import socket
import threading
import sys
import random
from plyer import notification
from text_encryption import encrypt_message, decrypt_message, derive_key

# Import external scripts here:
# Example: import other_script

SHARED_KEY = derive_key(123456)

clients = []

def handle_client(conn, addr):
  print(f"Client {addr} connected.")
  clients.append(conn)

  while True:
    try:
      data = conn.recv(4096)
      if not data:
        break

      payload = data[:-32]
      recv_hash = data[-32:]

      message = decrypt_message(payload, recv_hash, SHARED_KEY)
      print(f"\n[{addr}]: {message}")
      print("Your Message: ", end='', flush=True)
      notification.notify(title=f"New Message from {addr}", message={message}, app_name="PythoChat", timeout=10)

      broadcast(conn, message)
    except:
      break

  print(f"Client {addr} disconnected.")
  clients.remove(conn)
  conn.close()

def broadcast(sender_conn, message):
  payload, hash = encrypt_message(message, SHARED_KEY)
  data = payload + hash
  for client in clients:
    if client != sender_conn:
      try:
        client.sendall(data)
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
