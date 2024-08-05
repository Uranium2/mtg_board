import json

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory

from player.player import Player


class MTGServer(Protocol):
    def connectionMade(self):
        print("New connection")
        self.transport.write("Hello from the server".encode("utf-8"))

    def dataReceived(self, data):
        json_data = json.loads(data.decode())
        if json_data["class"] == "Player":
            data_class = Player.from_json(json_data)
        print(data_class)


class MTGServerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return MTGServer()


if __name__ == "__main__":
    reactor.listenTCP(8000, MTGServerFactory())
    reactor.run()
