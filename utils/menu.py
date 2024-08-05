import pygame_menu


# RightMenu Class
class RightMenu:
    def __init__(self, screen):
        self.menu = None
        self.screen = screen
        self.should_close = False
        self.button_settings = {
            "align": pygame_menu.locals.ALIGN_LEFT,
        }

    def move_to_board(self, card, deck):
        deck.move_to_board(card)
        self.should_close = True

    def move_to_hand(self, card, deck):
        deck.move_to_hand(card)
        self.should_close = True

    def draw_card(self, deck):
        deck.draw()
        self.should_close = True

    def exile_card(
        self,
        card,
        deck,
    ):
        deck.exile_card(card)
        self.should_close = True

    def move_to_graveyard(
        self,
        card,
        deck,
    ):
        deck.move_to_graveyard(card)
        self.should_close = True

    def create_menu(self, position, card, deck):
        my_theme = pygame_menu.themes.THEME_BLUE.copy()
        my_theme.title_font_size = 20
        self.menu = pygame_menu.Menu(
            "Card Options", 600, 200, theme=my_theme, verbose=False
        )
        self.should_close = False

        if deck.has_in_library(card):
            self.menu.add.button(
                "Draw Card", self.draw_card, deck, **self.button_settings
            )

        if not deck.has_in_board(card) and not deck.has_in_library(card):
            self.menu.add.button(
                "Move card to board",
                self.move_to_board,
                card,
                deck,
                **self.button_settings,
            )
        if not deck.has_in_hand(card):
            self.menu.add.button(
                "Move to hand", self.move_to_hand, card, deck, **self.button_settings
            )
        if not deck.has_in_exile(card):
            self.menu.add.button(
                "Exile card", self.exile_card, card, deck, **self.button_settings
            )
        if not deck.has_in_graveyard(card):
            self.menu.add.button(
                "Move card to graveyard",
                self.move_to_graveyard,
                card,
                deck,
                **self.button_settings,
            )

        # Adjust position if the menu goes out of screen bounds
        menu_width, menu_height = self.menu.get_size()
        screen_width, screen_height = self.screen.get_size()

        if position[0] + menu_width > screen_width:
            position = (screen_width - menu_width, position[1])
        if position[1] + menu_height > screen_height:
            position = (position[0], screen_height - menu_height)
        self.menu.set_absolute_position(
            position[0] + 25, position[1]
        )  # Patch, because I can not disable right click on bouttons...
        self.menu.enable()

    def update(self, events):
        if self.menu and self.menu.is_enabled():
            self.menu.update(events)
            self.menu.draw(self.screen)
