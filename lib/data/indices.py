from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass
class PageIndex:
    title: str
    source: str


@dataclass
class PageIndexWithTag:
    title: str
    tag: str
    source: str


@dataclass
class PageLang:
    src_lang: str
    dst_lang: str
    src_name: str
    dst_name: str
    source: str



@dataclass
class CVCharacter:
    name: str
    anime: str
    source: str

class GenderInfo(Enum):
    Male = 'male'
    Female = 'female'
    Other = 'other'
    Unknown = 'unknown'

@dataclass
class CVInfo:
    name: str
    gender: GenderInfo
    birth_year: int
    characters: List[CVCharacter]
    source: str


@dataclass
class AnimeInfo:
    name: str
    country: str
    author: List[str]
    design: List[str]
    production: List[str]
