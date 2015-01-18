import SocketServer
import json
import os
import sys
import uuid
import random

ADDRESS = "127.0.0.1"
PORT = 8080

FILE_SERVERS = {}
FILE_MAPPINGS = {}

def fileExists(filename):
    return filename in FILE_MAPPINGS

def getFileMapping(filename):
    if fileExists(filename):
        return FILE_MAPPINGS[filename]
    else:
        return None

def addFileMapping(filename, nodeID, address, port):
    FILE_MAPPINGS['filename'] = {"nodeID": nodeID, "address": address, "port": port}

def deleteFileMapping(filename):
    del FILE_MAPPINGS[filename]

def getRandomServer():
    index = random.randint(0, len(FILE_SERVERS)-1)
    return FILE_SERVERS.items()[index]

class ThreadedHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        msg = self.request.recv(1024)
        #print msg

        msg = json.loads(msg)
        requestType = msg['request']

        response = ""

        if requestType == "open":
            if fileExists(msg['filename']):
                fs = getFileMapping(msg['filename'])
                response = json.dumps({
                    "response": "open-exists",
                    "filename": msg['filename'],
                    "isFile": True,
                    "address": fs['address'],
                    "port": fs['port']
                })
            else:
                fs = getRandomServer()
                response = json.dumps({
                    "response": "open-null",
                    "filename": msg['filename'],
                    "isFile": False,
                    "uuid": fs[0],
                    "address": fs[1]['address'],
                    "port": fs[1]['port']
                })
        elif requestType == "close":
            response = json.dumps({
                "response": "close",
                "filename": msg['filename'],
                "isFile": True
            })
        elif requestType == "read":
            if fileExists(msg['filename']):
                fs = getFileMapping(filename)
                response = json.dumps({
                    "response": "read-exists",
                    "filename": msg['filename'],
                    "isFile": True,
                    "address": fs['address'],
                    "port": fs['port']
                })
            else:
                response = json.dumps({
                    "response": "read-null",
                    "filename": msg['filename'],
                    "isFile": False
                })        
        elif requestType == "write":
            print "write print something in master server"
            print msg['filename']
            print FILE_MAPPINGS
            if fileExists(msg['filename']):
                print "write if"
                fs = getFileMapping(msg['filename'])
                response = json.dumps({
                    "response": "write-exists",
                    "filename": msg['filename'],
                    "isFile": True,
                    "uuid": fs['uuid'],
                    "address": fs['address'],
                    "port": fs['port']
                })
            else:
                print "write else"
                fs = getRandomServer()
                #addFileMapping(msg['filename'], fs[0], fs[1]['address'], fs[1]['port'])
                FILE_MAPPINGS[msg['filename']] = {"uuid": fs[0], "address": fs[1]['address'], "port": fs[1]['port']}
                #print FILE_MAPPINGS
                response = json.dumps({
                    "response": "write-null",
                    "filename": msg['filename'],
                    "isFile": False,
                    "uuid": fs[0],
                    "address": fs[1]['address'],
                    "port": fs[1]['port']
                })
        elif requestType == "dfsjoin":
            nodeID = msg['uuid']
            # if evals to True the file server is new and a uuid will be generated
            # if evals to False the file server exists and already has a uuid
            if(nodeID == ""):
                nodeID = str(uuid.uuid4())

            FILE_SERVERS[nodeID] = {"address": msg['address'], "port": msg['port']}
            response = json.dumps({"response": requestType, "uuid": nodeID})
            print FILE_SERVERS
        else:
            response = json.dumps({"response": "error", "error": requestType+" is not a valid request"})

        self.request.sendall(response)


class MasterServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == '__main__':
    address = (ADDRESS, PORT)
    server = MasterServer(address, ThreadedHandler)
    server.serve_forever()