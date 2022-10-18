"""
Helper classes for TGTG items
"""

from typing import Dict, List


class Item:
    "TGTG item helper class"

    def __init__(self, json: dict) -> None:
        self.item_id: str = json["item"]["item_id"]
        self.display_name: str = json["display_name"]
        self.name: str = json["item"]["name"]
        self.store_name: str = json["store"]["store_name"]
        self.available: int = json["items_available"]

        price_data: dict = json["item"]["price_including_taxes"]

        self.price_int: int = price_data["minor_units"]
        self.price_float: float = price_data["minor_units"] / 100
        self.price_currency: str = price_data["code"]
        self.price: str = f"{self.price_float:.2f} {self.price_currency}"


# Used in get_item for when item_id is invalid
default_item = Item(
    {
        "item": {
            "item_id": "0",
            "name": "Unknown",
            "price_including_taxes": {"minor_units": 0, "code": "EUR"},
        },
        "store": {"store_name": "Unknown"},
        "display_name": "Unknown",
        "items_available": 0,
    }
)


class Items:
    "Helper class with list of all new items to check for new items"

    def __init__(self, json: List[dict]) -> None:
        self.items: Dict[str, Item] = {}

        for item_json in json:
            item = Item(item_json)
            self.items[item.item_id] = item

    def get_item(self, item_id: str) -> Item:
        "Get a specific item by its id"

        return self.items.get(item_id, default_item)

    def get_items(self) -> List[Item]:
        "Get all items"

        return list(self.items.values())

    def get_new_items(self, other: "Items") -> List[Item]:
        "Compare this list of items with another list of items and return the new items"

        new_items = []

        # Check if the new items have more boxes available than the old items
        for item in self.items.values():
            old_item = other.get_item(item.item_id)
            if item.available > old_item.available:
                new_items.append(item)

        return new_items
