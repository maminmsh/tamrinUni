import socket
import os
import gzip
import codecs

def rchunk(chunksize,filename,conSocket):
    f=codecs.open("/home/navid/ServerFiles/"+filename, "w", encoding='utf-8', errors='ignore')
    ans = str()
    if filename.split('.')[-1] == 'txt':
        try:
            while True:
                data = conSocket.recv(chunksize).decode()
                ans += data
                if not data or len(data) < chunksize:
                    break
        except Exception as e:
            print(e)
    else:
        try:
            ans=bytes()
            while True:
                data = conSocket.recv(chunksize)
                ans += data
                if not data or len(data) < chunksize:
                    break
        except Exception as e:
            print(e)
    data = gzip.decompress(ans)
    data2 = bytes.decode(data)
    f.write(data2)
    f.close()
        

serverPort = 8000
serverName = socket.gethostname()
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.settimeout(2)
name = input("Enter file name : ")
chunk_size = input("enter size of chunk : ")
path= input("Enter output path : ")
clientSocket.send(name.encode())
clientSocket.send(chunk_size.encode())
chunk_size2 = int(chunk_size)
status = clientSocket.recv(1024).decode()
print(status)
if status == "404 Not Found":
    print("No such file found")
else:
    completeName = os.path.join(path, name)
    rchunk(chunk_size2,path,clientSocket)

clientSocket.close()
