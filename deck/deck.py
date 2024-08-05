import random
from collections import deque

from deck.card import Card


class Deck:
    def __init__(self, commander, cards, screen):
        if len(cards) != 99:
            raise ValueError(
                f"A Commander deck must have exactly 99 cards. You have {len(cards)} cards"
            )
        self.commander = Card(
            commander, face_up=True, tapped=False, screen=screen, position=(1600, 700)
        )
        self.original_library = [
            Card(name=card_name, face_up=True, tapped=False, screen=screen)
            for card_name in cards
        ]
        self.reset_deck()
        self.screen_width, self.screen_height = screen.get_size()

    def reset_deck(self):
        self.library = deque(self.original_library)
        self.hand = []
        self.graveyard = []
        self.exile = []
        self.board = [self.commander]

    def render(self):

        # Draw hand
        for i, card in enumerate(self.hand):
            card.face_up = True
            card.tapped = False
            # card.update_position((0 + (i * 150), 900))
            card.display_card()

        # Draw players board
        for card in self.board:
            card.face_up = True
            card.display_card()

        if len(self.library) > 0:
            library_card = self.library[0]
            library_card.face_up = False
            library_card.tapped = False
            library_card.update_position((1600, 900))  # En bas a droite
            library_card.display_card()

        if len(self.graveyard) > 0:

            for i, graveyard_card in enumerate(self.graveyard):
                graveyard_card.face_up = True
                graveyard_card.tapped = False
                graveyard_card.update_position(
                    (1700, 900 + (i * 20))
                )  # En bas a droite
                graveyard_card.display_card()

    def shuffle(self):
        random.shuffle(self.library)

    def draw(self, count=1):
        for _ in range(count):
            if self.library:
                self.move_to_hand(self.library[0])
            else:
                print("No more cards in the library to draw.")

    def move_to_graveyard(self, card):
        if card in self.hand:
            self.hand.remove(card)
        elif card in self.library:
            self.library.remove(card)
        elif card in self.board:
            self.board.remove(card)
        else:
            print(f"{card} is not in hand, library, or on the board.")
            return
        self.graveyard.append(card)

    def move_to_hand(self, card):
        if card in self.library:
            self.library.remove(card)
        elif card in self.board:
            self.board.remove(card)
        elif card in self.graveyard:
            self.graveyard.remove(card)
        else:
            return
        self.hand.append(card)
        card.update_position((1400, 900))

    def exile_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
        elif card in self.library:
            self.library.remove(card)
        elif card in self.board:
            self.board.remove(card)
        elif card in self.graveyard:
            self.graveyard.remove(card)
        else:
            return
        self.exile.append(card)

    def move_to_board(self, card):
        if card in self.hand:
            self.hand.remove(card)
        elif card in self.graveyard:
            self.graveyard.remove(card)
        elif card in self.exile:
            self.exile.remove(card)
        elif card in self.library:
            self.library.remove(card)
        self.board.append(card)
        card_position = (self.screen_width // 2, self.screen_height // 2)
        card.update_position(card_position)

    def draw_initial_hand(self):
        self.reset_deck()
        self.shuffle()
        self.draw(7)
        for i, card in enumerate(self.hand):
            card.update_position((0 + (i * 150), 900))

    def has_in_board(self, card):
        return card in self.board

    def has_in_hand(self, card):
        return card in self.hand

    def has_in_exile(self, card):
        return card in self.exile

    def has_in_graveyard(self, card):
        return card in self.graveyard

    def has_in_library(self, card):
        return card in self.library

    def __repr__(self):
        return (
            f"Commander: {self.commander}\n"
            f"Hand: {self.hand}\n"
            f"Library: {len(self.library)} cards\n"
            f"Graveyard: {self.graveyard}\n"
            f"Exile: {self.exile}\n"
            f"Board: {self.board}"
        )
