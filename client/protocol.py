import struct
import time

message_types = {
	'CLIENT_GREETING': 1,
	'SERVER_ASSIGN': 2,
	'CLIENT_ASSIGN_ACK': 3,
	'SERVER_GREETING': 4,
	'CHAT_MESSAGE': 5,
}

def get_timestamp_ms():
	return time.time_ns() // 1000000

def make_header(msg_type, user_id, msg_id):
	ts = get_timestamp_ms()
	return struct.pack('!BBLQ', message_types[msg_type], user_id, msg_id, ts)

def read_header(hdr):
	return struct.unpack('!BBLQ', hdr)

message_type_rev = {
	1: 'CLIENT_GREETING',
	2: 'SERVER_ASSIGN',
	3: 'CLIENT_ASSIGN_ACK',
	4: 'SERVER_GREETING',
	5: 'CHAT_MESSAGE',
}
def debug_header(hdr):
	msg_type, user_id, msg_id, timestamp = read_header(hdr)
	return f'type = {message_type_rev[msg_type]}, user_id = {user_id}, msg_id = {msg_id}, timestamp = {timestamp}'
