import sys
import threading

import IP_Functionality.server as server
import IP_Functionality.client as client
import simulation

def run_host():
  try:
    server.server_script()
  except Exception as e:
    print(f"Host error: {e}")

def run_client():
  try:
    client.client_script()
  except Exception as e:
    print(f"Client error: {e}")

def run_simulation():
  try:
    simulation.simulate_text_messaging()
  except Exception as e:
    print(f"Simulation error: {e}")

def main():
  while True:
    print("\n=== Welcome to PythoChat ===")
    print("1. Host")
    print("2. Client")
    print("3. Simulate Cyberattack")
    print("4. Exit Application")

    choice = input("Select an option: ").strip()

    if choice == "1":
      run_host()
    elif choice == "2":
      run_client()
    elif choice == "3":
      # Replace with actual function
      print("Simulation is WIP, please select a different option.")
    elif choice == "4":
      sys.exit(0)
    else:
      print("Invalid selection. Try again.")

if __name__ == "__main__":
  main()
