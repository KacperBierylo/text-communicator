import sys
import socket
from PyQt5.QtWidgets import QApplication
from Window.MessageService import MessageService
from Window.ModelViewAplikation import ModelViewApliation


if __name__ == '__main__':
    host = socket.gethostname()
    #port = 1236
    port = int(sys.argv[1])
    messageService = MessageService(host,port)
    messageService.k.savepath = str(sys.argv[2])
    app = QApplication(sys.argv)
    window = ModelViewApliation(messageService)
    window.show()

    messageService.ModelView = window
    ### Funkcja która wyświetla wiadomośći od drugiej osoby
    ##messageService.receiveMessage("Wiadomośc","Tom",datetime.datetime.now())

    ### Funkcje która przetrzymuje dane w momencie wysłania wiadomości, aktualnie tylko wyświetla treść w konsoli w momencie klikniecia przycisku send
    #messageService.sendMessage()
    app.exec_()
