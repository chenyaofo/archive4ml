import uuid

class CustomUUID:
    def __init__(self, id_) -> None:
        if isinstance(id_, uuid.UUID):
            self.id_ = id_.__str__().replace("-", "")
        elif isinstance(id_, str):
            if len(id_) == 32:
                self.id_ = id_
        else:
            raise ValueError(f"Init from invalid uuid {id_}")

    @classmethod
    def from_random(cls):
        return cls(uuid.uuid4())
    
    @property
    def full_string(self):
        return self.id_
    
    @property
    def seperate_string(self):
        string = self.full_string
        return string[:2], string[2:4], string[4:]
    
    def __str__(self):
        return self.id_