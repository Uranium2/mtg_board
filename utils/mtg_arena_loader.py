from deck.deck import Deck


def load_deck_from_file(file_path, screen):
    """
    Loads a Magic the Gathering deck from a file and creates a Deck object.

    :param file_path: Path to the file containing the deck list
    :param screen: Pygame screen object
    :return: Deck object
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    cards = []
    commander = lines[0].split("(")[0].split(" ", 1)[1].strip()
    for line in lines[1:]:
        line = line.split("(")[0]
        line = line.split(" ")
        quantity = line[0]
        card_name = " ".join(line[1:])
        for i in range(int(quantity)):
            cards.append(card_name)
    if len(cards) != 99:
        raise ValueError("The deck must contain exactly 99 cards plus a commander.")

    return Deck(commander, cards, screen)
