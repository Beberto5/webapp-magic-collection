from sqlmodel import SQLModel, Field
from typing import Optional


class Card(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    scryfall_id: str = Field(unique=True, index=True)

    # Nome EN (sempre disponibile) + nome IT (quando esiste)
    name: str = Field(index=True)
    name_it: Optional[str] = Field(default=None, index=True)

    set_code: str = Field(index=True)
    set_name: str
    collector_number: str
    rarity: str = Field(index=True)
    type_line: str

    mana_cost: Optional[str] = None
    cmc: Optional[float] = None
    colors: Optional[str] = None
    color_identity: Optional[str] = None

    # Immagini EN
    image_uri: Optional[str] = None
    image_uri_small: Optional[str] = None

    # Immagini IT (None se non disponibili)
    image_uri_it: Optional[str] = None
    image_uri_small_it: Optional[str] = None

    oracle_text: Optional[str] = None


class CollectionEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    card_scryfall_id: str = Field(index=True, foreign_key="card.scryfall_id")
    quantity: int = Field(default=1)
