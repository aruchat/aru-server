from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class aruServer(WebSocket):
    clients = []
    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'disconnected')

def main():
    server = SimpleWebSocketServer('', 3000, aruServer)
    server.serveforever()

if __name__ == "__main__": main()
