import json
import uuid as iduu
from io import BytesIO
from pathlib import Path

import pygame
import requests
import scrython

RATIO = 1.396825396825397
HEIGHT = 150
WIDTH = HEIGHT / RATIO
CARD_SIZE = (WIDTH, HEIGHT)


class Card:
    def __init__(
        self,
        name,
        face_up=True,
        tapped=False,
        screen=None,
        uuid=None,
        position=None,
        url=None,
    ):
        self.name = name
        self.face_up = face_up
        self.tapped = tapped
        if not position:
            self.position = (0, 0)
        else:
            self.position = position
        self.url = url
        self.screen = screen
        self.rect = pygame.Rect(self.position, CARD_SIZE)
        if uuid:
            self.uuid = str(uuid)
        else:
            self.uuid = str(iduu.uuid4())
        self.img_front = self.load_image()
        self.img_back = self.load_back_image()

    def to_json(self):
        return json.dumps(
            {
                "class": "Card",
                "name": self.name,
                "face_up": self.face_up,
                "tapped": self.tapped,
                "position": self.position,
                "uuid": self.uuid,
                "url": self.url,
            }
        )

    @staticmethod
    def from_json(json_data, screen=None):
        data = json.loads(json_data)
        card = Card(
            name=data["name"],
            face_up=data["face_up"],
            tapped=data["tapped"],
            position=tuple(data["position"]),
            uuid=data["uuid"],
            screen=screen,
            url=data["url"],
        )
        return card

    def fetch_image_url(self):
        if self.url:
            return
        try:
            print(f"Getting {self.name} from scrython")
            card = scrython.cards.Named(fuzzy=self.name)
            self.url = card.image_uris()["normal"]
        except Exception as e:
            print(f"Error fetching image URL for {self.name}: {e}")
            # For debugging
            self.url = "https://cards.scryfall.io/normal/front/3/2/326679a2-782d-45a0-9a06-b147ceff3979.jpg?1584831563"
            # return None

    def __repr__(self):
        return f"""uuid: {self.uuid} name: {self.name}:
        Rect:{self.rect},
        Face-up: {self.face_up},
        Tapped: {self.tapped},
        url: {self.url},
        pos: {self.position}.
        """

    def load_image(self):
        image_file = f"data/{self.name}.jpg"
        image_file = image_file.replace("//", "")
        my_file = Path(image_file)
        if not self.url:
            self.fetch_image_url()
        if not my_file.is_file():
            response = requests.get(self.url)
            content = response.content
            open(image_file, "wb").write(content)
            print(f"{image_file} saved")
            image_file = BytesIO(content)
        else:
            print(f"Use local cache image for {self.name}")
        image = pygame.image.load(image_file)
        image = pygame.transform.scale(image, CARD_SIZE)
        return image

    def load_back_image(self):
        image = pygame.image.load("data/back.jpg")
        image = pygame.transform.scale(image, CARD_SIZE)
        return image

    def display_card(self):
        if self.face_up:
            card_image = self.img_front
        else:
            card_image = self.img_back
        if self.tapped:
            card_image = pygame.transform.rotate(card_image, 90)
        self.screen.blit(card_image, self.position)
        self.rect.topleft = self.position

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update_position(self, new_position):
        self.position = new_position
        self.rect.topleft = new_position
