# This file is very likely to change a lot, this is more of a basic idea of what we will need to implement.

import socket
import threading
import sys
from plyer import notification
from text_encryption import encrypt_message, decrypt_message, derive_key

# External scripts go here:
# Examples:
#   import other_script
#   import

SHARED_KEY = derive_key(123456)

def recieve_data(sock):
  # Acts like the server version, but instead receives data from the server.
  while True:
    try:
      data = sock.recv(4096)
      if not data:
        break
      # Logic for determining type of data. Requires the use of external scripts to decrypt messages.
      # For testing we will use text first.
      payload = data[:-32]
      recv_hash = data[-32:]
      message = decrypt_message(payload, recv_hash, SHARED_KEY)

      print(f"\n[Server]: {message}")
      print("Your Message: ", end='', flush=True)
      notification.notify(title="New Message from Server", message={message}, app_name="PythoChat", timeout=10)
    except:
      break
  print("Server has disconnected")
  sock.close()

def send_data(sock):
  while True:
    try:
      message = input("Your Message: ")
      if message.lower() == "exit":
        print("Exiting...")
        payload, hash = encrypt_message(message, SHARED_KEY)
        sock.sendall(payload + hash)
    except:
      break

  sock.close()



def client_script():
  host = input("Enter the IP ADDRESS value: ")
  port = input("Enter the PORT value: ")
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((host, port))
  print(f"\nConnected to {host}:{port}")

  # Receive thread goes here. It will handle receiving data.
  threading.Thread(target=recieve_data, args=(client_socket,), daemon=True).start()
  # Send thread logic goes here. Will probably just be a while loop.
  threading.Thread(target=send_data, args=(client_socket,), daemon=True).start()

  while True:
    if(not client_socket.fileno()):
      break
  
  client_socket.close()

if __name__ == '__main__':
  client_script()
  
