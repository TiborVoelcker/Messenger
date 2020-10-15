# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 13:09:19 2019

@author: tibor
"""

import socket
import select

class Server():
    def __init__(self):
        self.HEADER_LENGTH = 10
        self.KEY_HEADER_LENGTH = 3
        self.hostname = socket.gethostname()
        self.IP = socket.gethostbyname(self.hostname)
        self.PORT = 2000

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen()
        
        self.sockets_list = [self.server_socket]
        
        self.clients = {}

    def run(self):
        print(f"Server launched.\nIP: {self.IP}\nHostname: {self.hostname}\nPort: {self.PORT}\n")
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
        
            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_addr = self.server_socket.accept()

                    if len(self.sockets_list) > 2:
                        message = "ERROR: Sorry, there are already two Clients connected to the server.".encode('utf-8')
                        message_header = f"{len(message) :< {self.HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header + message)
                        continue

                    self.sockets_list.append(client_socket)

        
                    self.clients[client_socket] = client_addr

                    print(f"Accepted new connection from {client_addr[0]}:{client_addr[1]}")

                else:
                    message = self.receive_message(notified_socket)
            
                    if not message:
                        print(f"Closed connection from {client_addr[0]}:{client_addr[1]}")
                        self.sockets_list.remove(notified_socket)
                        del self.clients[notified_socket]
                        continue

                    print(f"Message recieved: {message['data']}")

                    self.send_all(message, notified_socket)

            for notified_socket in exception_sockets:
                self.sockets_list.remove(notified_socket)
                del self.clients[notified_socket]

    def send_all(self, message, notified_socket):
        for client_socket in self.clients:
            if client_socket != notified_socket:
                client_socket.send(message['header'] + message['data'])

    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(self.HEADER_LENGTH)

            if message_header.decode('utf-8') == "NEW_CLIENT" or message_header.decode('utf-8') == "OLD_CLIENT":
                key_header = client_socket.recv(self.KEY_HEADER_LENGTH)
                key = client_socket.recv(int(key_header.decode('utf-8')))
                return {'header': message_header, 'data': key_header + key}

            if not len(message_header):
                return False

            else:
                message_length = int(message_header.decode('utf-8'))
                return {"header": message_header, "data": client_socket.recv(message_length)}
    
        except:
            return False

server = Server()
server.run()
