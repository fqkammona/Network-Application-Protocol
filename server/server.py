import socket

def main():
    serverPort = 12000
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            serverSocket.bind(('', serverPort))
            serverSocket.listen(1)
            print(f"The server is ready to receive on port {serverPort}")

            while True:
                connectionSocket, addr = serverSocket.accept()
                print(f"Connection established with {addr}")

                # Server-side handshaking
                client_handshake = connectionSocket.recv(1024).decode()
                if client_handshake == "HELLO_SERVER":
                    print(f"Handshake initiated by {addr}")
                    connectionSocket.send("HELLO_CLIENT".encode())

                    # Wait for client's final acknowledgment
                    client_ack = connectionSocket.recv(1024).decode()
                    if client_ack == "CLIENT_ACK":
                        print(f"Handshake completed with {addr}")
                    else:
                        print(f"Handshake failed with {addr}")
                        connectionSocket.close()
                        continue
                else:
                    print(f"Unexpected message from {addr}, handshake failed.")
                    connectionSocket.close()
                    continue

                while True:
                    message = connectionSocket.recv(1024).decode()
                    if not message or message.lower() == "quit":
                        print(f"Connection with {addr} closed.")
                        break

                    print(f"Received from {addr}: {message}")
                    response = f"Server received: {message}"
                    connectionSocket.send(response.encode())

                connectionSocket.close()

    # When Control C is entered the server completely shuts down
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
    
if __name__ == "__main__":
    main()
