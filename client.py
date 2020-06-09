import socket

host = "localhost"
port = 2004

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect((host, port))

while True:
    data = tcp_client.recv(1000)
    print("Odebrano komunikat: ", data.decode(), end="")

tcp_client.close()