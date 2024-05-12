# client_gui.py
import socket
import threading
import tkinter as tk


def receive_messages():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            msg_list.insert(tk.END, msg)
        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            break


def send_message(event=None):
    msg = my_msg.get()
    my_msg.set("")  # Clear input field
    client_socket.send(msg.encode("utf-8"))


def on_closing(event=None):
    my_msg.set("exit")
    send_message()


# Main client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5555))

# GUI setup
client_root = tk.Tk()
client_root.title("Chat Application")
client_root.geometry("400x400")

# Frame for received messages
messages_frame = tk.Frame(client_root)
messages_frame.pack(fill=tk.BOTH, expand=True)

msg_list = tk.Listbox(messages_frame, height=15, width=50)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

scrollbar = tk.Scrollbar(messages_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar.config(command=msg_list.yview)

msg_list.config(yscrollcommand=scrollbar.set)

# Frame for sending messages
entry_frame = tk.Frame(client_root)
entry_frame.pack(fill=tk.X, padx=10, pady=10)

my_msg = tk.StringVar()
entry_field = tk.Entry(entry_frame, textvariable=my_msg)
entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True)

send_button = tk.Button(entry_frame, text="Send",
                        command=send_message, bg="#4CAF50", fg="white")
send_button.pack(side=tk.RIGHT)

# Close the connection when the client GUI window is closed


def close_window():
    client_socket.close()
    client_root.destroy()


client_root.protocol("WM_DELETE_WINDOW", close_window)

# Start a thread to receive messages from server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

tk.mainloop()
