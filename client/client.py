import sys
import socket

def main():
    if len(sys.argv) < 3:
        print("Usage: python client.py <ServerName> <ServerPort>")
        return

    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect((serverName, serverPort))

        while True:
            message = input("Enter message (type 'quit' to exit): ")
            clientSocket.send(message.encode())

            if message.lower() == "quit":
                break

            response = clientSocket.recv(1024).decode()
            print(f"From Server: {response}")

if __name__ == "__main__":
    main()
