import socket
import sys
from datetime import datetime

from protocol import message_types, make_header, read_header, debug_header

def readable_ts(ts):
    return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')

def do_handshake(sock, username):
    # Handshake part 1, CLIENT_GREETING
    client_greeting = make_header('CLIENT_GREETING', 0, 0) + username.encode()
    sock.send(client_greeting)

    # Handshake part 2, SERVER_ASSIGN
    server_assign = sock.recv(1024)
    print(f'Received message: {debug_header(server_assign)}')
    msg_type, user_id, message_id, timestamp = read_header(server_assign)

    if msg_type != message_types['SERVER_ASSIGN']:
        raise Exception(f'unexpected server message ({msg_type})')

    print(f'Server assigned user id {user_id} ({readable_ts(timestamp)})')

    # Handshake part 3, CLIENT_ASSIGN_ACK
    client_assign_ack = make_header('CLIENT_ASSIGN_ACK', user_id, 0)
    sock.send(client_assign_ack)

    # Handshake part 4, SERVER_GREETING
    server_greeting = sock.recv(1024)
    print(f'Received message: {debug_header(server_greeting[:14])}')
    msg_type, server_user_id, message_id, timestamp = read_header(server_greeting[:14])

    if msg_type != message_types['SERVER_GREETING']:
        raise Exception(f'unexpected server message ({msg_type})')

    server_username = server_greeting[14:].decode()
    print(f'Server username is {server_username} ({readable_ts(timestamp)})')
    print(f'Handshake copmlete\n')

    return (user_id, server_user_id, server_username)

def main(addr, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((addr, port))

        username = input('What username would you like to use? ')
        uid, server_uid, server_username = do_handshake(sock, username)

        message_id = 1 << 31 # client messages have MSB set to 1

        while True:
            chat_message = input(f"Enter message to {server_username} (type 'quit' to exit): ")
            hdr = make_header('CHAT_MESSAGE', uid, message_id)
            message_id += 1

            msg = hdr + chat_message.encode()
            sock.send(msg)

            if chat_message.lower() == "quit":
                break

            response = sock.recv(1024)
            response_hdr = response[:14]
            response_data = response[14:].decode()
            print(f'[debug] received headers: {debug_header(response_hdr)}')
            print(f"{server_username}> {response_data}")
            print()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client.py <ServerName> <ServerPort>")
        sys.exit(1)

    addr = sys.argv[1]
    port = int(sys.argv[2])

    main(addr, port)
