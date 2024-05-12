# server_gui.py
import socket
import threading
import tkinter as tk

# Function to handle client connections


def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    client_listbox.insert(tk.END, f"{address[0]}:{address[1]}")

    while True:
        # Receive message from client
        msg = client_socket.recv(1024).decode("utf-8")
        if not msg or msg.lower() == "exit":
            break

        # Broadcast message to all clients
        print(f"[{address}] {msg}")
        broadcast(msg)

    # Close connection
    client_socket.close()
    client_listbox.delete(0, tk.END)
    for client in clients:
        client_listbox.insert(tk.END, f"{client[0]}:{client[1]}")
    print(f"[DISCONNECTED] {address} disconnected.")

# Function to broadcast message to all clients


def broadcast(msg):
    for client in clients:
        client[2].send(msg.encode("utf-8"))

# Function to send message from server to client


def send_message(event=None):
    msg = server_msg.get()
    server_msg.set("")  # Clear input field
    broadcast("[SERVER] " + msg)


# Main server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(5)

print("[SERVER] Server is listening...")

clients = []

# Accept incoming connections


def accept_connections():
    while True:
        client_socket, address = server.accept()
        clients.append((address[0], address[1], client_socket))
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, address))
        client_thread.start()


# Start accepting connections in a separate thread
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# GUI setup
server_root = tk.Tk()
server_root.title("Server Window")

# Frame for clients list
clients_frame = tk.Frame(server_root)
clients_frame.pack(side=tk.LEFT, padx=10)

client_label = tk.Label(
    clients_frame, text="Clients Connected:", font=("Helvetica", 12))
client_label.pack(pady=10)

client_listbox = tk.Listbox(clients_frame, height=10, width=30)
client_listbox.pack()

# Frame for server messages
server_frame = tk.Frame(server_root)
server_frame.pack(side=tk.RIGHT, padx=10)

server_msg_label = tk.Label(
    server_frame, text="Send message to clients:", font=("Helvetica", 12))
server_msg_label.pack(pady=10)

server_msg = tk.StringVar()
server_msg_entry = tk.Entry(server_frame, textvariable=server_msg)
server_msg_entry.pack()

send_button = tk.Button(server_frame, text="Send",
                        command=send_message, bg="#4CAF50", fg="white")
send_button.pack()

server_root.mainloop()
