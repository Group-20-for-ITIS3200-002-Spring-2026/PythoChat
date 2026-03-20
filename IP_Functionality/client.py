# This file is very likely to change a lot, this is more of a basic idea of what we will need to implement.

import socket
import threading
import sys
from plyer import notification

# External scripts go here:
# Examples:
#   import other_script
#   import

def recieve_data(sock):
  # Acts like the server version, but instead receives data from the server.
  while True:
    try:
      data = sock.recv(1024)
      if not data:
        break
      # Logic for determining type of data. Requires the use of external scripts to decrypt messages.
      # For testing we will use text first.
      print(f"\n[Server]: {data}")
      print("Your Message: ", end='', flush=True)
    except:
      break
  print("Server has disconnected")
  sock.close()

def client_script():
  host = input("Enter the IP ADDRESS value: ")
  port = input("Enter the PORT value: ")
  client_socket = socket.socket()
  client_socket.connect((host, port))
  print(f"\nConnected to {host}:{port}")

  # Receive thread goes here. It will handle receiving data.
  #     Start Here
  # Send thread logic goes here. Will probably just be a while loop.
  #     Start Here
  
  client_socket.close()

if __name__ = '__main__':
  client_script()
  
