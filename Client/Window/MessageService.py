import rsa

from Window.ModelViewAplikation import ModelViewApliation
import socket
import json

from klient import klient


class MessageService:
    ModelView: ModelViewApliation
    k:klient = 0
    keyServer = 0

    def __init__(self,host,port):
        self.k = klient(self,host,port)

    def sendMessage(self, message, author, time):
        self.k.sendMessage(message,time)

    def receiveMessage(self, message, author, time):
        self.ModelView.message_from(message, author, time)

    def changeTypeCode( self,type ):
        self.k.kodowanie = type

    def sendFile(self, filepath):
        self.k.sendFile(filepath)