from typing import List

class Item:
    def __init__(self, json) -> None:
        self.id = json["item"]["item_id"]
        self.name = json["display_name"]
        self.available = json["items_available"]

default_item = Item({"item": {"item_id": "0"}, "display_name": "Unknown", "items_available": 0})

class Items:
    def __init__(self, json) -> None:
        self.items = {}

        for item in json:
            item = Item(item)
            self.items[item.id] = item
    
    def get_item(self, item_id) -> Item:
        return self.items.get(item_id, default_item)
    
    def get_new_items(self, other) -> List[Item]:
        new_items = []
        
        for item in self.items.values():
            old_item = other.get_item(item.id)
            if item.available > old_item.available:
                new_items.append(item)

        return new_items