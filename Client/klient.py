import os
from base64 import b64decode
from base64 import b64encode
import hashlib
import socket
import threading
import json
import datetime
import rsa
from Crypto.Cipher import AES
from Crypto import Random
import time
from Window.ProgressBar import ProgressBar
from Crypto.Cipher import AES
import hashlib
import os, random, struct
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s : s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s : s[:-ord(s[len(s) - 1 :])]

def generateSesionKey():
    sesion_key = hashlib.sha256((Random.get_random_bytes(8))).digest()
    #print("Sesion key")
    #print(sesion_key)
    t = encryptUseSesionKeyECB("test",sesion_key)
    d = dencryptUseSesionKeyECB(t,sesion_key)
    print("testing" + d)
    return sesion_key

def encryptUseSesionKeyCBC(test,key): ##MODE_CBC MODE_ECB
    iv = Random.new().read(AES.block_size)
    raw = pad(str(test)).encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out = b64encode(iv + cipher.encrypt(raw))
    return out

def encryptUseSesionKeyECB(test,key): ##MODE_CBC MODE_ECB
    raw = pad(str(test))
    cipher = AES.new(key, AES.MODE_ECB)
    out = b64encode(cipher.encrypt(raw.encode('utf-8')))
    return out

def dencryptUseSesionKeyCBC(tekst,key):
    try:
        enc = b64decode(tekst)
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        out = unpad(cipher.decrypt(enc[16 :]))
        return str(out)
    except:
        print("Użyj dekodowanie ECB")
        return "ZLE KODOWANIE"

def dencryptUseSesionKeyECB(tekst,key):
    try:
        enc = b64decode(tekst)
        cipher = AES.new(key, AES.MODE_ECB)
        msg = unpad(cipher.decrypt(enc)).decode('utf8')
        return msg
    except:
        print("uzyj dekodowanie CBC")
        return "ZLE KODOWANIE"



def encryptKey ( raw, password ) :
    ##private_key = hashlib.sha256(password.encode("utf-8")).digest()
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(str(raw)).encode("utf-8")
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(raw))

def decryptKey ( enc, password ) :
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16 :]))


def encrypt_file(key, in_filename, mode, out_filename=None, chunksize=64*1024):

    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = Random.new().read(AES.block_size)
    #print(iv)
    if mode == "CBC":
        encryptor = AES.new(key, AES.MODE_CBC, iv)
    elif mode == "ECB":
        encryptor = AES.new(key, AES.MODE_ECB)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename,mode, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        print(mode)
        if mode == "CBC":
            print("cbc dekryptor")
            decryptor = AES.new(key, AES.MODE_CBC, iv)
        elif mode == "ECB":
            decryptor = AES.new(key, AES.MODE_ECB)
            print("ecb dekryptor")
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


def odbieraj (ms,_s,k):
    incoming_message = _s.recv(4096)
    k.sendMessage2(k.publicKey.save_pkcs1("PEM"))
    file = 0
    received = 0

    while 1:
        incoming_message = _s.recv(4096)
        incoming_message = incoming_message.decode()
        if(incoming_message == "KEYGEN"):
            incoming_message = _s.recv(4096)
            incoming_message = rsa.PublicKey.load_pkcs1(incoming_message)
            k.sesionKey = generateSesionKey()
            incoming_message = encrypt(k.sesionKey,incoming_message)
            k.sendMessage2(incoming_message)
            print("Wygenerowany klucz sesj")
        if(incoming_message == "KEYSESION"):
            incoming_message = _s.recv(4096)
            k.sesionKey = generateSesionKey()#descrypt(incoming_message,k.privateKey)
            print("Przypisano klucz sesji")
        if(incoming_message == "AUTHO"):
            while 1:
                incoming_message = _s.recv(4096)
                print("odebrano")
                if incoming_message == b'\x00':
                    print("poczatek")
                    file = 1
                    filedata = _s.recv(4096)
                    filedata = filedata.decode()
                    filename, filesize = filedata.split(",")
                    filesize = int(filesize)
                    f = open(k.savepath + filename, "wb")
                if file == 0:
                    print("nie plik")
                    if(k.kodowanie == "ECB"):
                        incoming_message = dencryptUseSesionKeyECB(incoming_message, k.sesionKey)
                    elif(k.kodowanie == "CBC"):
                        incoming_message = dencryptUseSesionKeyCBC(incoming_message, k.sesionKey)
                        incoming_message = incoming_message[2:-1]
                    time = datetime.datetime.now()
                    osoba = "HE"
                    #print("Odebrana wiadomosc: " + str(incoming_message))
                    ms.receiveMessage(incoming_message, osoba, time)
                # if incoming_message == b'\x00':
                #     print("!dupa!")
                if file == 1 and incoming_message != b'\x00':


                    print("odbieram porcje")
                    #print("wiadomosc: " + str(incoming_message))
                    f.write(incoming_message)
                    received += 4096
                    print("Otrzymano: " + str(received))
                    if received >= filesize:
                        print("przeslano")
                        file = 0
                        received = 0
                        f.close()
                        decrypt_file(k.sesionKey, filename, k.kodowanie, k.savepath + filename[:-4])
                        os.remove(k.savepath + filename)


def encrypt(message, keyServery):
    return rsa.encrypt(message,keyServery)

def descrypt(message,privateKey):##dekodkowanie
    try:
        return rsa.decrypt(message,privateKey)
    except:
        return False

password = input("Enter password: ")

class klient:
    _s:socket
    _ms = 0
    publicKey:rsa.PublicKey
    privateKey:rsa.PrivateKey
    serverKey:rsa.PublicKey
    sesionKey = 0
    kodowanie = "CBC"
    savepath = "C:\\obrazki1\\"

    def __init__(self,ms,host,port):
        self.generateKey()
        self._ms = ms
        self._s = socket.socket()
        self._s.connect((host, port))
        print("connected to server")
        self.odbieranie = threading.Thread(target=odbieraj, args=(ms,self._s,self))
        self.odbieranie.start()

    def sendMessage(self,message,time):
        ##message = [message, self.port, time]
        ##message = json.dumps(message)
        if(self.kodowanie == "ECB"):
            incoming_message = encryptUseSesionKeyECB(message, self.sesionKey)
        elif(self.kodowanie == "CBC"):
            incoming_message = encryptUseSesionKeyCBC(message, self.sesionKey)
        print("Wysłana wiadomosc" + str(incoming_message))
        self._s.send(incoming_message)

    def sendMessage3(self, message):
        ##message = [message, self.port, time]
        ##message = json.dumps(message)

        print("Wysłana wiadomosc" + str(message))
        self._s.send(message)

    def sendMessage2(self,message):
        ##message = [message, self.port, time]
        ##message = json.dumps(message)
        self._s.send(message)

    def generateKey(self):
        self.publicKey, self.privateKey = rsa.newkeys(1024)
        encrypted = encryptKey(self.publicKey.save_pkcs1('PEM'), password)
        descypted = decryptKey(encrypted,password)
        key = bytes(descypted)
        #dopisać odczytywanie z pliku

    def sendFile(self, filepath):
        filename = os.path.basename(filepath)
        pb = ProgressBar()
        encrypted_file = encrypt_file(self.sesionKey,filepath, self.kodowanie, filename + ".enc")
        file_size = os.path.getsize(filename + ".enc")

        self._s.send(b'\x00')
        #time.sleep(1)
        self._s.send(str(filename + ".enc" + "," + str(file_size)).encode())
        #time.sleep(1)
        print("Wysyłanie...")
        f = open(filepath, "rb")
        read_size = 4096
        bytes = f.read(read_size)
        read = len(bytes)
        while bytes:
            # f2.write(bytes)
            message = bytes
            #self._s.send(message)
            self.sendMessage3(message)
            print("Przesłano " + str(("{:.0f}".format(read / file_size * 100))) + "%")
            pb.setValue(int(str(("{:.0f}".format(read / file_size * 100)))))
            bytes = f.read(read_size)
            # print(len(bytes))
            read += len(bytes)
        f.close()
        #time.sleep(0.5)
        os.remove(filename + ".enc")