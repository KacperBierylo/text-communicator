import socket
import threading
import sys
import time
import json
import rsa

connected = []


class client:
    connect = 0
    publicKey = 0
    autho = False;

    def __init__(self,connected,pK):
        self.connect = connected
        self.publicKey = pK

def encrypt (message,key ) :
    return rsa.encrypt(message.encode('utf-8'), key)

def descrypt (message ) :  ##dekodkowanie
    try:
        return rsa.decrypt(message, privateKey).decode("utf-8")
    except :
        return False

def generateKey():
    publicKey, privateKey = rsa.newkeys(1024)
    return publicKey,privateKey
publicKey,privateKey = generateKey()


def odbieraj(sender:socket.socket, receivers:list):
    while 1:
        Autho = False
        incoming_message = sender.recv(4096)
        for receiver in receivers:
            if sender == receiver.connect:
                if receiver.autho == False:
                    incoming_message = incoming_message.decode()
                    Autho = True
               # if receiver.autho == True:
                    #incoming_message = descrypt(incoming_message)
                   # print("Otrzymano wiadomosc od " + str(sender.getpeername()))
        for receiver in receivers:
            if sender == receiver.connect and receiver.autho==False and Autho == True:
                if(len(connected)==1):
                    print("Otrzymano publiczny klucz" + str(sender.getpeername()))
                    receiver.publicKey = incoming_message
                elif(len(connected)==2):
                    print("Generuje klucz sesji" + str(sender.getpeername()))
                    message = "KEYGEN"
                    #time.sleep(1)
                    receiver.connect.send(message.encode())
                    #time.sleep(1)
                    receiver.connect.send(receivers[0].publicKey.encode())
                    incoming_message = sender.recv(4096)
                    message = "KEYSESION"
                    #time.sleep(1)
                    receivers[0].connect.send(message.encode())
                    #time.sleep(1)
                    receivers[0].connect.send(incoming_message)
                    message = "AUTHO"
                    message = message.encode()
                    #time.sleep(1)
                    receiver.connect.send(message)
                    #time.sleep(1)
                    receivers[0].connect.send(message)
                    print("Rozpoczeto czat")
                receiver.autho = True
                break
            if sender != receiver.connect and receiver.autho==True and Autho == False:
                receiver.connect.send(incoming_message)
        #time.sleep(1)

def odbieraj2(sender:socket.socket, receivers):
    while 1:
        Autho = False
        incoming_message = sender.recv(4096)
        for receiver in receivers:
            if sender == receiver.connect:
                if receiver.autho == False:
                    incoming_message = incoming_message.decode()
                    Autho = True
                if receiver.autho == True:
                    incoming_message = descrypt(incoming_message)
                    print(incoming_message)
        #incoming_message = json.loads(incoming_message)
        #incoming_message = json.dumps(incoming_message)
        for receiver in receivers:
            if sender == receiver.connect and receiver.autho==False and Autho == True:

                print("Otrzymano autoryzacje" + str(sender.getpeername()))
                receiver.publicKey = rsa.PublicKey.load_pkcs1(incoming_message)
                receiver.autho = True
                break
            if sender != receiver.connect and receiver.autho==True and Autho == False:
                message = encrypt(incoming_message,receiver.publicKey)
                receiver.connect.send(message)
        #time.sleep(1)


def sendKey(conn:socket):
    key = publicKey.save_pkcs1("PEM")
    conn.send(key)

def nasluchuj(host, port):
    print("nasluchuje na porcie: " + str(port))
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    k = client(conn,0)
    connected.append(k)
    sendKey(conn)
    print(addr, "has connected")
    odbieranie = threading.Thread(target=odbieraj, args=(conn, connected))
    odbieranie.start()


generateKey()

host = socket.gethostname()
open_sockets_number = 3
nasluchiwania = []
for i in range(open_sockets_number):
    nasluchiwania.append(threading.Thread(target=nasluchuj, args=(host, 1234 + i)))
    nasluchiwania[i].start()