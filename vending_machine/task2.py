import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.sendto('111'.encode(), ('127.0.0.1', 63154))
sock.close()
