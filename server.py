import uuid as iduu

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory


class MTGServer(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.uuid = str(iduu.uuid4())

    def __repr__(self):
        return f"MTGServer UUID {self.uuid}"

    def connectionMade(self):
        print("New connection")
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Connection lost")
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        self.broadcast_message(data)

    def broadcast_message(self, data):
        for client in self.factory.clients:
            if client != self:
                print("Sending Data")
                client.transport.write(data)


class MTGServerFactory(ServerFactory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return MTGServer(self)


if __name__ == "__main__":
    port = 8000
    reactor.listenTCP(port, MTGServerFactory())
    print(f"Server Running on port {port}")
    reactor.run()
