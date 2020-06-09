import socket
from threading import Thread
import random
import time
from datetime import datetime

TCP_IP = "0.0.0.0"
TCP_PORT = 2004

##### klasa generujaca dane ######
class RandomData(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.counter = 1
        self.result = ""

    def run(self):
        while True:
            ticker = "MBK"
            value = random.randrange(300,400) + random.random()
            now = datetime.now().strftime("%Y%m%d%H%m%S")
            self.result = f"{self.counter};{ticker};{now};{value:.2f}\n"
            self.counter += 1
            time.sleep(random.randrange(2,10))

    def get_data(self):
        return self.result


##### klasa obslugi klienta ######
class ClientThread(Thread):
    def __init__(self, conn, ip, port, datasource):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.datasource = datasource
        print("Utworzono nowy wątek serwera dla klienta IP="+ip+" z portu: "+str(port))

    def run(self):
        prev_value = None
        while True:
            result = self.datasource.get_data()
            if (result!=prev_value):
                self.conn.send(result.encode())
                prev_value = result
                time.sleep(1)

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_server.bind((TCP_IP, TCP_PORT))

threads = []

datathread = RandomData()
datathread.start()

print("Oczekiwanie na połączenie.....")
while True:
    tcp_server.listen()
    (conn, (ip, port)) = tcp_server.accept()
    # utworz watek obslugi - nowy obiekt klasy Thread
    new_thread = ClientThread(conn, ip, port, datathread)
    new_thread.start()
    threads.append(new_thread)

datathread.join()
for t in threads:
    t.join()
