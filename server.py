import socket

def main():
    # Set the server's port number
    serverPort = 12000  

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        # Bind the socket to the port
        serverSocket.bind(('', serverPort))
        
        # Listen for incoming connections
        serverSocket.listen(1)
        print(f"The server is ready to receive on port {serverPort}")
        
        # Keep the server running forever
        while True:
            # Wait for a connection
            connectionSocket, addr = serverSocket.accept()
            
            # Receive data from the client
            message = connectionSocket.recv(1024).decode()
            print(f"Received from {addr}: {message}")

            if message == "quit":
                print("Server received termination signal. Closing connection.")
                connectionSocket.close()
                break
            else:
                # Send a response back to the client
                response = f"Message received: {message}"
                connectionSocket.send(response.encode())
            
            # Close the connection
            connectionSocket.close()

if __name__ == "__main__":
    main()
