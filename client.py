import pygame
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall

from player.player import Player
from utils.menu import RightMenu
from utils.mtg_arena_loader import load_deck_from_file

# from utils.menu import Menu


DESIRED_FPS = 10.0  # 30 frames per second


class CardGameClientProtocol(Protocol):
    def __init__(self, factory, player):
        self.factory = factory
        self.player = player

    def connectionMade(self):
        # Store a reference to this protocol instance
        self.factory.protocol_instance = self
        print("Connected to server")
        self.transport.write(self.player.to_json().encode())

    def dataReceived(self, data):
        message = data.decode()
        print(f"Received: {message}")

    def send_data(self, data):
        self.transport.write(data.encode())


class CardGameClientFactory(ClientFactory):
    def __init__(self, player):
        self.player = player
        self.protocol_instance = None

    def buildProtocol(self, addr):
        return CardGameClientProtocol(self, self.player)


dragging = False
offset = (0, 0)
selected_card = None
menu = None


def game_tick(factory):
    global dragging, offset, selected_card, menu_opened

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            print("Quit event detected, stopping reactor and exiting.")
            pygame.quit()
            reactor.stop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu.menu and menu.menu.is_enabled():
                menu_rect = pygame.Rect(
                    menu.menu.get_position()[0],
                    menu.menu.get_position()[1],
                    menu.menu.get_width(),
                    menu.menu.get_height(),
                )
                if not menu_rect.collidepoint(event.pos):
                    menu.menu.disable()
                else:
                    continue  # Skip the rest of the logic if the click was inside the menu

            if event.button == 1:  # LEFT CLICK
                for cards in [deck.board, deck.hand, deck.graveyard]:
                    for card in cards:
                        if card.is_clicked(event.pos):
                            dragging = True
                            selected_card = card
                            offset = (
                                card.position[0] - event.pos[0],
                                card.position[1] - event.pos[1],
                            )
                            break
            elif event.button == 3:  # RIGHT CLICK
                for cards in [deck.board, deck.hand, deck.graveyard, deck.library]:
                    for card in cards:
                        if card.is_clicked(event.pos):
                            print(card)
                            menu.create_menu(event.pos, card, deck)
                            selected_card = card
                            break

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            selected_card = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging and selected_card:
                new_position = (event.pos[0] + offset[0], event.pos[1] + offset[1])
                selected_card.update_position(new_position)

    if factory.protocol_instance:
        factory.protocol_instance.send_data(deck.to_json())

    if menu.menu and menu.menu.is_enabled() and menu.should_close:
        menu.menu.disable()

    screen.fill("black")

    # Render all cards
    deck.render()

    if menu:
        menu.update(events)

    pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    # Get the current display info
    info = pygame.display.Info()

    # Set the display mode to the real screen size
    screen = pygame.display.set_mode((info.current_w, info.current_h))
    # screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("MTG Client")

    commander = "Atraxa, Praetors' Voice"
    card_names = ["Plains" for i in range(99)]

    menu = RightMenu(screen)

    deck = load_deck_from_file("data/decks/1.txt", screen)

    deck.draw_initial_hand()

    player = Player(user_name="Antoine")
    factory = CardGameClientFactory(player)
    # Start Twisted client
    reactor.connectTCP("localhost", 8000, factory)

    tick = LoopingCall(game_tick, factory)
    tick.start(1.0 / DESIRED_FPS)

    reactor.run()
