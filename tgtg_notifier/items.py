from typing import List

class Item:
    def __init__(self, json: dict) -> None:
        self.id: str = json["item"]["item_id"]
        self.name: str = json["display_name"]
        self.available: int = json["items_available"]

default_item = Item({"item": {"item_id": "0"}, "display_name": "Unknown", "items_available": 0})

class Items:
    def __init__(self, json: List[dict]) -> None:
        self.items = {}

        for item_json in json:
            item = Item(item_json)
            self.items[item.id] = item
    
    def get_item(self, item_id: str) -> Item:
        return self.items.get(item_id, default_item)
    
    def get_new_items(self, other: 'Items') -> List[Item]:
        new_items = []
        
        # Check if the new items have more boxes available than the old items
        for item in self.items.values():
            old_item = other.get_item(item.id)
            if item.available > old_item.available:
                new_items.append(item)

        return new_items