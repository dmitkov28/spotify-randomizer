import json
import os
import random
from typing import List
import httpx
from bs4 import BeautifulSoup, Tag
import re


def get_all_genres(path: str = "genres.json"):
    url = "https://everynoise.com/everynoise1d.html"
    res = httpx.get(url)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    a_tags = table.find_all("a") if isinstance(table, Tag) else []
    genres = [
        a.get_text(strip=True) for a in a_tags if a.get_text(strip=True) != "\u260a"
    ]
    with open(path, "w") as f:
        json.dump(genres, f)


def load_genres(path: str = "genres.json"):
    if not os.path.exists(path):
        get_all_genres()

    with open(path, "r") as f:
        genres = json.load(f)
    return genres


def pick_random_genres(n_genres: int = 1, genres: List[str] = load_genres()):
    return random.choices(genres, k=n_genres)


def is_similar(a: str, b: str) -> bool:
    a_lower = a.lower()
    b_lower = b.lower()

    if a_lower in b_lower or b_lower in a_lower:
        return True

    a_words = re.findall(r"\w+", a_lower)
    b_words = re.findall(r"\w+", b_lower)
    for word in a_words:
        if word in b_lower:
            return True
    for word in b_words:
        if word in a_lower:
            return True
    return False


def filter_genres(target: str, genres: List[str] = load_genres()):
    return list(filter(lambda genre: is_similar(target, genre), genres))
