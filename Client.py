# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 13:41:34 2019

@author: tibor
"""

import socket
import errno
import sys
from DiffieHellman import DiffieHellman
from Crypto.Cipher import Blowfish

class Client():
    def __init__(self):
        self.HEADER_LENGTH = 10
        self.KEY_HEADER_LENGTH = 3
        self.IP = "127.0.0.1"
        self.PORT = 1234
        self.dif = DiffieHellman()

    def run(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.IP, self.PORT))
        self.client_socket.setblocking(False)
        self.key_protocol_send("NEW")
        self.Enc = Blowfish.new("0000")

    def receive(self):
        try:
            while True:
                message_header = self.client_socket.recv(self.HEADER_LENGTH)
                if message_header.decode('utf-8') == "NEW_CLIENT":
                    return self.key_protocol_receive("NEW")
                if message_header.decode('utf-8') == "OLD_CLIENT":
                    return self.key_protocol_receive("OLD")
                else:
                    message_length = int(message_header.decode('utf-8'))
                    message = self.client_socket.recv(message_length)
                    if message[:5] == b'ERROR':
                        return message.decode('utf-8')
                    message = self.Enc.decrypt(message)

                    try:
                        return message.decode('utf-8').strip()
                    except UnicodeDecodeError:
                        return "Encryption problem. Decryption not possible."

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("Reading error", str(e))
                sys.exit()
            else:
                pass

        except Exception as e:
            print("General error", str(e))
            sys.exit()

    def send(self, plain):
        pad = 8 - len(plain.encode('utf-8')) % 8
        plain = plain + " "*pad
        message = self.Enc.encrypt(plain)
        message_header = f"{len(message) :< {self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + message)

    def key_protocol_send(self, tag):
        pub_key = str(self.dif.pub_key).encode('utf-8')
        key_header = f"{len(pub_key) :< {self.KEY_HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(f"{tag}_CLIENT".encode('utf-8') + key_header + pub_key)

    def key_protocol_receive(self, tag):
        key_header = self.client_socket.recv(self.KEY_HEADER_LENGTH)
        key_length = int(key_header.decode('utf-8'))
        pub_key = self.client_socket.recv(key_length).decode('utf-8')
        self.Enc = Blowfish.new(str(self.dif.calcKey(pub_key)%448))
        if tag == "NEW": self.key_protocol_send("OLD")
        return "Secure Connection Established"

    def close(self):
        self.client_socket.close()

