from dataclasses import dataclass
from typing import Any, Mapping, Optional


def _to_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


@dataclass(frozen=True)
class UserProfile:
    user_id: int
    name: Optional[str] = None
    number: Optional[str] = None
    age: Optional[int] = None

    @property
    def is_complete(self) -> bool:
        return all((self.name, self.number, self.age is not None))

    @property
    def is_adult(self) -> bool:
        return self.age is not None and self.age >= 18

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "UserProfile":
        return cls(
            user_id=int(document["user_id"]),
            name=document.get("name"),
            number=document.get("number"),
            age=_to_int(document.get("age")),
        )


@dataclass(frozen=True)
class Category:
    title: str

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "Category":
        return cls(title=str(document["title"]))


@dataclass(frozen=True)
class Subcategory:
    title: str
    category_title: str

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "Subcategory":
        return cls(
            title=str(document["title"]),
            category_title=str(document["categories"]),
        )


@dataclass(frozen=True)
class Product:
    title: str
    description: str
    price: int
    category_title: str
    file_name: Optional[str] = None

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "Product":
        return cls(
            title=str(document["title"]),
            description=str(document.get("description", "")),
            price=int(document["price"]),
            category_title=str(document["categories"]),
            file_name=document.get("file"),
        )


@dataclass(frozen=True)
class CartItem:
    user_id: int
    product: str
    description: str
    price: int

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "CartItem":
        return cls(
            user_id=int(document["user_id"]),
            product=str(document["product"]),
            description=str(document.get("description", "")),
            price=int(document["price"]),
        )


@dataclass(frozen=True)
class Order:
    user_id: int
    product: str
    price: int
    track: str
    status: str

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "Order":
        return cls(
            user_id=int(document["user_id"]),
            product=str(document["product"]),
            price=int(document["price"]),
            track=str(document["track"]),
            status=str(document["status"]),
        )
