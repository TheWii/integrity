__version__ = "0.9.0"

from .api import Integrity as _Integrity
from .components import Components as _Components
from .hooks import Hook as _Hook
from .plugin import beet_default

__all__ = ["Component", "beet_default"]
