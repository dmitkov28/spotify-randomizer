from enum import Enum
from pydantic import BaseModel
from typing import List, Union
from datetime import datetime


class AlbumTypeEnum(Enum):
    ALBUM = "album"
    SINGLE = "single"


class ExternalUrls(BaseModel):
    spotify: str


class ArtistType(Enum):
    ARTIST = "artist"


class Artist(BaseModel):
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: ArtistType
    uri: str


class Image(BaseModel):
    height: int
    width: int
    url: str


class ReleaseDatePrecision(Enum):
    DAY = "day"
    YEAR = "year"


class Album(BaseModel):
    album_type: AlbumTypeEnum
    artists: List[Artist]
    available_markets: List[str]
    external_urls: ExternalUrls
    href: str
    id: str
    images: List[Image]
    is_playable: bool
    name: str
    release_date: Union[datetime, int]
    release_date_precision: ReleaseDatePrecision
    total_tracks: int
    type: AlbumTypeEnum
    uri: str


class ExternalIDS(BaseModel):
    isrc: str


class ItemType(Enum):
    TRACK = "track"


class Item(BaseModel):
    album: Album
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIDS
    external_urls: ExternalUrls
    href: str
    id: str
    is_local: bool
    is_playable: bool
    name: str
    popularity: int
    preview_url: None
    track_number: int
    type: ItemType
    uri: str


class Tracks(BaseModel):
    href: str
    limit: int
    next: str
    offset: int
    previous: None
    total: int
    items: List[Item]


class Country(BaseModel):
    tracks: Tracks
