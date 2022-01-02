from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, Undefined
from typing import Optional

from dataclasses_json.cfg import config

def exclude_none():
    return field(default=None, metadata=config(exclude=lambda x: x is None))

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Metadata:
    title: Optional[str] = exclude_none()
    subtitle: Optional[str] = exclude_none()
    artist: Optional[str] = exclude_none()
    genre: Optional[str] = exclude_none()
    designer: Optional[str] = exclude_none()
    difficulty: Optional[str] = exclude_none()
    playlevel: Optional[str] = exclude_none()
    songid: Optional[str] = exclude_none()
    wave: Optional[str] = exclude_none()
    waveoffset: Optional[float] = exclude_none()
    jacket: Optional[str] = exclude_none()
    background: Optional[str] = exclude_none()
    movie: Optional[str] = exclude_none()
    movieoffset: Optional[float] = exclude_none()
    basebpm: Optional[float] = exclude_none()
    requests: Optional[list[str]] = exclude_none()

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Note:
    tick: int
    lane: int
    width: int
    type: int

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Score:
    metadata: Metadata
    taps: list[Note]
    directionals: list[Note]
    slides: list[list[Note]]
    bpms: list[tuple[int, float]]
    bar_lengths: list[tuple[int, float]]