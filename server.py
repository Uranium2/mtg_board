from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory


class MTGServer(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("New connection")
        self.factory.clients.append(self)
        self.transport.write("Hello from the server".encode("utf-8"))

    def connectionLost(self, reason):
        print("Connection lost")
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        message = data.decode()
        self.broadcast_message(message)

    def broadcast_message(self, message):
        for client in self.factory.clients:
            if client != self:
                client.transport.write(f"Broadcast: {message}".encode("utf-8"))


class MTGServerFactory(ServerFactory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return MTGServer(self)


if __name__ == "__main__":
    reactor.listenTCP(8000, MTGServerFactory())
    reactor.run()
