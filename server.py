import socket
import threading

# 保存所有活跃的客户端连接
clients = []

def broadcast_message(message, _conn):
    for client in clients:
        if client != _conn:
            try:
                client.send(message)
            except:
                client.close()
                # 如果链接不可用，则将其移除
                clients.remove(client)

def client_thread(conn, address):
    conn.send("Welcome to the chatroom!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(1024)
            if message:
                print(f"{address} says: {message.decode('utf-8')}")
                broadcast_message(message, conn)
            else:
                conn.close()
                clients.remove(conn)
                broadcast_message(f"{address} has left the chat room.".encode('utf-8'), conn)
                break
        except:
            continue

def server_program():
    host = '0.0.0.0'
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server is listening on port {port}...")

    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)
        print(f"{addr} has connected.")
        threading.Thread(target=client_thread, args=(conn, addr)).start()

if __name__ == '__main__':
    server_program()
