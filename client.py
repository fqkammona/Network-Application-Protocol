import sys
import socket

def main():
    # Ensure that the server name and port number are provided
    if len(sys.argv) < 4:
        print("Usage: python client.py <ServerName> <ServerPort> <Message>")
        return

    serverName = sys.argv[1]        # Server IP address
    serverPort = int(sys.argv[2])   # Port number of the server to connect to
    message = sys.argv[3]           # Message to send to the server

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        # Connect to the server
        clientSocket.connect((serverName, serverPort))
        
        # Send a message to the server
        clientSocket.send(message.encode())

        # Receive the server response
        response = clientSocket.recv(1024).decode()
        print(f"From Server: {response}")

        # Close the connection (done implicitly by the with statement)

if __name__ == "__main__":
    main()

