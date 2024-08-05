import json
import uuid as iduu


class Player:
    def __init__(self, user_name, uuid=None):
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = iduu.uuid4()

        self.user_name = user_name

    def to_json(self):
        return json.dumps(
            {"class": "Player", "user_name": self.user_name, "uuid": str(self.uuid)}
        )

    @staticmethod
    def from_json(json_data):
        player = Player(json_data["user_name"], json_data["uuid"])
        return player

    def __repr__(self):
        return f"Player(uuid={self.uuid}, user_name={self.user_name})"
