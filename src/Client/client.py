import socket
import sys
import json
import argparse
import uuid
import time

MASTER_ADDRESS = "127.0.0.1"
MASTER_PORT = 8080
LOCK_ADDRESS = "127.0.0.1"
LOCK_PORT = 8888

class DFSClient():
    def __init__(self, masterHost, masterPort, lockHost, lockPort):
        self.id = str(uuid.uuid4())
        self.masterAddr = masterHost
        self.masterPort = masterPort
        self.lockAddr = lockHost
        self.lockPort = lockPort
        self.cache = {}

    def open(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.masterAddr, self.masterPort))

        msg = json.dumps({"request": "open", "filename": filename, "clientid": self.id})
        sock.sendall(msg)
        response = sock.recv(1024)

        return response

    def close(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.masterAddr, self.masterPort))

        msg = json.dumps({"request": "close", "filename": filename, "clientid": self.id})
        sock.sendall(msg)
        response = sock.recv(1024)
        return response

    def checkLock(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.lockAddr, self.lockPort))

        msg = json.dumps({"request": "checklock", "filename": filename, "clientid": self.id})
        sock.sendall(msg)
        response = sock.recv(1024)

        return response

    def obtainLock(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.lockAddr, self.lockPort))

        msg = json.dumps({"request": "obtainlock", "filename": filename, "clientid": self.id})
        sock.sendall(msg)
        response = sock.recv(1024)

        return response

    def read(self, filename):
        fileServerInfo = json.loads(self.open(filename))

        # if file exists, checked with directory server
        if fileServerInfo['isFile']:
            # if file is in cache and its timestamp is at least as new as the last write to the file
            if (filename in self.cache) and (self.cache[filename]['timestamp'] >= fileServerInfo['timestamp']):
                cacheFileInfo = self.cache[filename]
                print "Read '" + filename + "' from cache!"
                return cacheFileInfo
            else:
                addr = fileServerInfo['address']
                port = int(fileServerInfo['port'])

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((addr, port))

                msg = json.dumps({"request": "read", "filename": filename, "clientid": self.id})
                sock.sendall(msg)

                response = sock.recv(1024)

                self.cache['filename'] = json.loads(response)

                return response
        else:
        	return filename + " does not exist!"

    # 1. check master server for location on data nodes
    # 2. check if file is locked (whether by someone else or this client)
    # 3. if not locked, write file, otherwise only write if current client owns lock (tbi)
    def write(self, filename, data):
        lockcheck = json.loads(client.checkLock(filename))

        if lockcheck['response'] == "locked":
            return "Cannot write as file is locked by another client!"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.masterAddr, self.masterPort))

        timestamp = time.time() 

        msg = json.dumps({"request": "write", "filename": filename, "clientid": self.id, "timestamp": timestamp})
        sock.sendall(msg)
        response = sock.recv(1024)

        fileServerInfo = json.loads(response)

        addr = fileServerInfo['address']
        port = int(fileServerInfo['port'])

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr, port))

        content = {"request": "write", "filename": filename, "data": data, "clientid": self.id, "timestamp": timestamp}

        self.cache[filename] = content

        msg = json.dumps(content)
        sock.sendall(msg)

        response = sock.recv(1024)
        return response


# simple test for the client library
if __name__ == '__main__':
    client = DFSClient(MASTER_ADDRESS, MASTER_PORT, LOCK_ADDRESS, LOCK_PORT)

    requestType = ""
    response = ""

    while requestType != "exit":
        requestType = raw_input("Please enter a request type [open/close/checklock/obtainlock/read/write] or type exit to quit: ")

        if requestType == "open":
            filename = raw_input("Please enter the filename: ")
            response = client.open(filename)
        elif requestType == "close":
            filename = raw_input("Please enter the filename: ")
            response = client.close(filename)
        elif requestType == "checklock":
            filename = raw_input("Please enter the filename: ")
            response = client.checkLock(filename)
        elif requestType == "obtainlock":
            filename = raw_input("Please enter the filename: ")
            response = client.obtainLock(filename)
        elif requestType == "read":
            filename = raw_input("Please enter the filename: ")
            response = client.read(filename)
        elif requestType == "write":
            filename = raw_input("Please enter the filename: ")
            data = raw_input("Please enter the file contents to write: ")
            response = client.write(filename, data)
        elif requestType == "exit":
            response = "Exiting Distributed File System!"
        else:
            response = "Not a valid request type, please try again."

        print response