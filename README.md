# PythoChat
Python-based Secure MMS Application with Cyberattack Simulation.

# Instructions:
When running the executable, you will be given 4 options:

1. Host - This creates a server which will allow you to connect multiple clients (SUCCESS CASE).
2. Client - This allows you to act as a client which makes you connect to a server to chat with other clients (SUCCESS CASE).
3. Simulate Cyberattack - This allows you to simulate a cyberattack (FAILURE CASE).
4. Exit Application - This allows you to exit the application.

Choose the option you would like. If you chose Host, input 0.0.0.0 to allow a connection from any network adapter. If you chose Client, input the IP address of the server machine's IP address. If you don't know what your machine's IP address is, type the following into your terminal:
1. Mac/Linux: ifconfig
2. Windows: ipconfig

NOTE: If you are unable to connect between two computers (one with Host and one with Client), make sure that your firewall is disabled, as it will prevent the file from working properly, and also change your network profile type to the "Private" option.

# Build
For 6, input the following lines in the Command Line Interface, replacing main.py with the main python file name:

```
python pythochat_main.py
pip install pyinstaller
python -m PyInstaller --onefile pythochat_main.py
```

This will create a *dist* folder containing *pythochat_main.exe*, which is an executable file. If you already have pyinstaller installed and you don't need to test the file, ignore lines 1 & 2 and only run line 3.
