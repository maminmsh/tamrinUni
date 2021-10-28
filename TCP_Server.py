import socket
import os
import os.path
import gzip
import codecs

def schunk(chunksize,filename,conSocket):
    f = codecs.open("/home/navid/ServerFiles/"+filename,'r', encoding='utf-8', errors='ignore')
    conSocket.settimeout(2)
    if filename.split('.')[-1] == 'txt':
        while True:
            data = f.read(chunksize)
            conSocket.send(data.encode())
            if not data or len(data) < chunksize:
                break
    else:
        while True:
            data = f.read(chunksize)
            conSocket.send(gzip.compress(bytes(data, encoding='utf-8')))
            if not data or len(data) < chunksize:
                break

serverPort = 8000
serverName = socket.gethostname()
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverName,serverPort))
serverSocket.listen(3)
print("The Server is ready to receive")



while True:
    connectionSocket, addr = serverSocket.accept()
    name  = connectionSocket.recv(1024).decode()
    chunk_size = int(connectionSocket.recv(1024).decode())
    files = os.listdir("/home/navid/ServerFiles/")
    if name in files:
        connectionSocket.send("200ok".encode())
        schunk(chunk_size, name, connectionSocket)
    else:
        connectionSocket.send("404 Not Found".encode())
    
    connectionSocket.close()

