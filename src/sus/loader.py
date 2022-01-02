import logging
import re

from collections import defaultdict
from typing import Callable, TextIO
from .schemas import Score, Note, Metadata

logger = logging.getLogger(__name__)

def process_metadata(lines: list[tuple[str]]) -> Metadata:
    result = {}
    for line in lines:
        if len(line) == 2:
            key, value = line
        else:
            key = line[0]
            value = None
        key = key[1:]
        value = value.strip('"') if value != None else None
        if key == 'TITLE':
            result['title'] = value
        elif key == 'SUBTITLE':
            result['subtitle'] = value
        elif key == 'ARTIST':
            result['artist'] = value
        elif key == 'GENRE':
            result['genre'] = value
        elif key == 'DESIGNER':
            result['designer'] = value
        elif key == 'DIFFICULTY':
            result['difficulty'] = value
        elif key == 'PLAYLEVEL':
            result['playlevel'] = value
        elif key == 'SONGID':
            result['songid'] = value
        elif key == 'WAVE':
            result['wave'] = value
        elif key == 'WAVEOFFSET':
            result['waveoffset'] = float(value)
        elif key == 'JACKET':
            result['jacket'] = value
        elif key == 'BACKGROUND':
            result['background'] = value
        elif key == 'MOVIE':
            result['movie'] = value
        elif key == 'MOVIEOFFSET':
            result['movieoffset'] = float(value)
        elif key == 'BASEBPM':
            result['basebpm'] = float(value)
        elif key == 'REQUEST':
            if 'requests' not in result:
                result['requests'] = []
            result['requests'].append(value)
    return Metadata.from_dict(result)

def process_score(lines: list[tuple[str]], metadata: list[tuple[str]]) -> Score:
    processed_metadata = process_metadata(metadata)

    try:
        ticks_per_beat_request = [int(request.split()[1]) for request in processed_metadata.requests if request.startswith('ticks_per_beat')] if processed_metadata.requests else []
        ticks_per_beat = ticks_per_beat_request[0]
    except IndexError:
        logger.warning('No ticks_per_beat request found, defaulting to 480.')
        ticks_per_beat = 480
    
    bar_lengths: list[tuple[int, float]] = []    
    for header, data in lines:
        if len(header) == 5 and header.endswith('02') and header.isdigit():
            bar_lengths.append((int(header[0:3]), float(data)))
    
    sorted_bar_lengths = sorted(bar_lengths, key=lambda x: x[0])

    ticks = 0
    
    bars = list(reversed(
        [
            (
                measure, beats * ticks_per_beat,
                ticks := ticks +
                    ((measure - sorted_bar_lengths[i - 1][0]) * sorted_bar_lengths[i - 1][1] * ticks_per_beat if i > 0 else 0)
            ) for i, (measure, beats) in enumerate(sorted_bar_lengths)
        ]
    ))
    
    def to_tick(measure: int, i: int, total: int) -> int:
        bar = next(bar for bar in bars if measure >= bar[0])
        if not bar: raise ValueError(f'Measure {measure} is out of range.')
        (bar_measure, ticks_per_measure, ticks) = bar
        
        return ticks + (measure - bar_measure) * ticks_per_measure + (i * ticks_per_measure) / total

    bpm_map = {}
    bpm_change_objects = []
    tap_notes = []
    directional_notes = []
    streams = defaultdict(list)

    for header, data in lines:
        if (len(header) == 5 and header.startswith('BPM')):
            bpm_map[header[3:]] = float(data)
        elif (len(header) == 5 and header.endswith('08')):
            bpm_change_objects += to_raw_objects(header, data, to_tick)
        elif (len(header) == 5 and header[3] == '1'):
            tap_notes += to_note_objects(header, data, to_tick)
        elif (len(header) == 6 and header[3] == '3'):
            channel = header[5]
            streams[channel] += to_note_objects(header, data, to_tick)
        elif (len(header) == 5 and header[3] == '5'):
            directional_notes += to_note_objects(header, data, to_tick)
            

    slide_notes = []
    for stream in streams.values():
        slide_notes += to_slides(stream)
    
    bpms = [
        (tick, bpm_map[value] or 0)
        for tick, value in
        sorted(bpm_change_objects, key=lambda x: x[0])
    ]
    
    return Score(
        metadata=processed_metadata,
        taps=tap_notes,
        directionals=directional_notes,
        slides=slide_notes,
        bpms=bpms,
        bar_lengths=bar_lengths
    )
    
def to_slides(stream: list[Note]) -> list[list[Note]]:
    slides: list[list[Note]] = []  
    current: list[Note] = None
    for note in sorted(stream, key=lambda x: x.tick):
        if not current:
            current = []
            slides.append(current)

        current.append(note)
        
        if note.type == 2:
            current = None
    return slides

def to_note_objects(header: int, data: str, to_tick: Callable[[int, int, int], int]) -> list[Note]:
    return [
        Note(
            tick=tick,
            lane=int(header[4], 36),
            width=int(value[1], 36),
            type=int(value[0], 36),
        )
        for tick, value in to_raw_objects(header, data, to_tick)
    ]

def to_raw_objects(header: int, data: str, to_tick: Callable[[int, int, int], int]) -> list[tuple[int, str]]:
    measure = int(header[:3])
    values = list(enumerate(re.findall(r'.{2}', data)))
    return [
        (to_tick(measure, i, len(values)), value)
        for i, value in values
        if value != '00'
    ]

def load(fp: TextIO) -> Score:
    return loads(fp.read())

def loads(data: str) -> Score:
    """
    Parse SUS data into a Score object.

    :param data: The score data.
    :return: A Score object.
    """
    metadata = []
    scoredata = []
    for line in data.splitlines():
        if not line.startswith('#'):
            continue
        line = line.strip()
        match = re.match(r'^#(\w+):\s*(.*)$', line)
        if match:
            scoredata.append(match.groups())
        else:
            metadata.append(tuple(line.split(' ', 1)))

    return process_score(scoredata, metadata)