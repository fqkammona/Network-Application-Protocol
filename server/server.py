import socket
import sys
from datetime import datetime

from protocol import message_types, make_header, read_header, debug_header

def readable_ts(ts):
    return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')

def do_handshake(sock, client_uid, username):
    # Handshake part 1, CLIENT_GREETING
    client_greeting = sock.recv(1024)
    print(f'Received message: {debug_header(client_greeting[:14])}')
    msg_type, _, _, timestamp = read_header(client_greeting[:14])

    if msg_type != message_types['CLIENT_GREETING']:
        raise Exception(f'unexpected client message ({msg_type})')

    client_username = client_greeting[14:].decode()
    print(f'Client username is {client_username} ({readable_ts(timestamp)})')

    # Handshake part 2, SERVER_ASSIGN
    server_assign = make_header('SERVER_ASSIGN', client_uid, 0)
    sock.send(server_assign)

    # Handshake part 3, CLIENT_ASSIGN_ACK
    client_assign_ack = sock.recv(1024)
    print(f'Received message: {debug_header(client_assign_ack)}')
    msg_type, user_id, _, timestamp = read_header(client_assign_ack)

    if msg_type != message_types['CLIENT_ASSIGN_ACK']:
        raise Exception(f'unexpected client message ({msg_type})')
    elif user_id != client_uid:
        raise Exception(f'client failed to acknowledge correct user id')

    print(f'Client acknowledged user id {user_id} ({readable_ts(timestamp)})')

    # Handshake part 4, SERVER_GREETING
    server_greeting = make_header('SERVER_GREETING', 0, 0) + username.encode()
    sock.send(server_greeting)
    print(f'Handshake copmlete\n')

    return client_username

def main(port):
    client_uid = 32
    username = input('What username would you like to use? ')
    message_id = 1

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('', port))
            sock.listen(1)
            print(f"The server is ready to receive on port {port}")

            while True:
                conn_sock, addr = sock.accept()
                print(f"Connection established with client {addr}")

                client_username = do_handshake(conn_sock, client_uid, username)
                client_uid += 1

                while True:
                    response = conn_sock.recv(1024)
                    response_hdr = response[:14]
                    response_data = response[14:].decode()
                    print(f'[debug] received headers: {debug_header(response_hdr)}')

                    if response_data.lower() == "quit":
                        print(f"Connection with {client_username} closed.")
                        break

                    print(f"{client_username}> {response_data}")

                    chat_message = input(f"Enter message to {client_username}: ")
                    hdr = make_header('CHAT_MESSAGE', 0, message_id)
                    message_id += 1

                    msg = hdr + chat_message.encode()
                    conn_sock.send(msg)
                    print()

                conn_sock.close()

    # When Control C is entered the server completely shuts down
    except KeyboardInterrupt:
        print("\nServer is shutting down.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python server.py <ServerPort>")
        sys.exit(1)

    port = int(sys.argv[1])

    main(port)
