"""
Helper classes for TGTG items
"""

from typing import List


class Item:
    "TGTG item helper class"

    def __init__(self, json: dict) -> None:
        self.item_id: str = json["item"]["item_id"]
        self.name: str = json["display_name"]
        self.available: int = json["items_available"]


default_item = Item(
    {"item": {"item_id": "0"}, "display_name": "Unknown", "items_available": 0}
)


class Items:
    "Helper class with list of all new items to check for new items"

    def __init__(self, json: List[dict]) -> None:
        self.items = {}

        for item_json in json:
            item = Item(item_json)
            self.items[item.item_id] = item

    def get_item(self, item_id: str) -> Item:
        "Get a specific item by its id"

        return self.items.get(item_id, default_item)

    def get_new_items(self, other: "Items") -> List[Item]:
        "Compare this list of items with another list of items and return the new items"

        new_items = []

        # Check if the new items have more boxes available than the old items
        for item in self.items.values():
            old_item = other.get_item(item.item_id)
            if item.available > old_item.available:
                new_items.append(item)

        return new_items
