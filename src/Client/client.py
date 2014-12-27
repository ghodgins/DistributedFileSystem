import socket
import sys
import json
import argparse

class DFSClient():
    def __init__(self, host, port):
        self.masterAddr = host
        self.masterPort = port

    def open(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.masterAddr, self.masterPort))

        msg = json.dumps({"request": "open", "filename": filename})
        sock.sendall(msg)
        response = sock.recv(1024)

        return response

    def close(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.masterAddr, self.masterPort))

        msg = json.dumps({"request": "close", "filename": filename})
        sock.sendall(msg)
        response = sock.recv(1024)
        return response

    def read(self, filename):
        fileServerInfo = json.loads(self.open(filename))

        if fileServerInfo['isFile']:
	        addr = fileServerInfo['address']
	        port = int(fileServerInfo['port'])

	        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	        sock.connect((addr, port))

	        msg = json.dumps({"request": "read", "filename": filename})
	        sock.sendall(msg)

	        response = sock.recv(1024)
	        return response
        else:
        	return filename + " does not exist!"

    def write(self, filename, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.masterAddr, self.masterPort))

        msg = json.dumps({"request": "write", "filename": filename})
        sock.sendall(msg)
        response = sock.recv(1024)

        fileServerInfo = json.loads(response)

        addr = fileServerInfo['address']
        port = int(fileServerInfo['port'])

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr, port))

        msg = json.dumps({"request": "write", "filename": filename, "data": data})
        sock.sendall(msg)

        response = sock.recv(1024)
        return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client for testing Distribute File System.')
    parser.add_argument('masterAddr', metavar='address', type=str, help='Address of master server')
    parser.add_argument('masterPort', metavar='port', type=int, help='Port of master server')

    args = parser.parse_args()

    client = DFSClient(args.masterAddr, args.masterPort)

    requestType = ""
    response = ""

    while requestType != "exit":
        requestType = raw_input("Please enter a request type [open/close/read/write] or type exit to quit: ")

        if requestType == "open":
            filename = raw_input("Please enter the filename: ")
            response = client.open(filename)
        elif requestType == "close":
            filename = raw_input("Please enter the filename: ")
            response = client.close(filename)
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