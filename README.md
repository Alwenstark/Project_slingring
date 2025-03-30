# SlingRing

## Overview
SlingRing is a Python-based remote shell that allows command execution on a remote system using sockets. It supports basic shell commands, file upload, and file download functionalities.

## Features
- Remote command execution
- File upload from client to server
- File download from server to client
- Directory navigation (cd command)

## Prerequisites
- Python 3.x

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Alwenstark/Project_slingring.git
   cd Project_slingring
   ```

2. Run the script:
   - To start as a listener (server):
     ```sh
     python3 slingring.py
     ```
   - To start as a client:
     ```sh
     python3 slingring.py
     ```

## Usage
1. **Start the server:**
   - Choose `l` when prompted.
   - Enter the IP and port to bind the listener.
2. **Connect the client:**
   - Choose `c` when prompted.
   - Enter the server IP and port.
3. **Execute commands:**
   - Type shell commands to execute on the remote machine.
   - Use `upload <filename>` to transfer files from client to server.
   - Use `download <filename>` to retrieve files from server to client.
   - Use `exit` to close the connection.

## Disclaimer
This tool is for educational purposes only. Unauthorized use is prohibited.

