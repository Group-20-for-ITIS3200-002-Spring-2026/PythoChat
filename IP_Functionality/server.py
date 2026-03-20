# Found these based on research of Python libraries. May/May Not Use all of them.
import socket
import threading
import sys
import random
from plyer import notification

# Import external scripts here:
# Example: import other_script

def recieve_data():
  # Handles recieving data from client
  while True:
    try:
      data = conn.recv(1024)
      if not data:
        break
      # Logic for determining type of data. Requires the use of external scripts to decrypt messages.
      # For testing we will use text first.
      print(f"\n[Client]: {data}")
      print("Your Message: ", end='', flush=True)
      notification.notify(title="New Message!", message={data}, app_name="PythoChat", timeout=10)
    except:
      break
  print("Client has disconnected.")
  conn.close()

# Host value is IP of the user's input.
# May use port value as a randomly-generated value above 1024 and at most 65000.
def server_script():
  # To be implemented.

if __name__ = "__main__":
  reciever_script()
