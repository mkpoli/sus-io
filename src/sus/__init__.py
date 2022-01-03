from pathlib import Path
from single_source import get_version

__version__ = get_version(__name__, Path(__file__).parent.parent.parent)
__all__ = ['load', 'dump', 'loads', 'dumps']

from .loader import load, loads
from .dumper import dump, dumps