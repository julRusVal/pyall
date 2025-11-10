"""
Public package interface for the legacy `pyall` module.

Historically, users interacted with a single ``pyall.py`` file.  By keeping
the canonical implementation inside :mod:`pyall.pyall` and re-exporting the
symbols here, we maintain backwards compatibility while embracing a modern
``src``-based package layout.
"""

from . import pyall as _legacy_pyall
from .pyall import *  # noqa: F401,F403
from .datamodel import NavigationRecord, BeamXYZ88, XYZ88Datagram, PointCloud

# Keep a reference to the legacy module so code can still access ``pyall.pyall``.
pyall = _legacy_pyall

__all__ = [name for name in dir(_legacy_pyall) if not name.startswith("_")]
__all__ += ["NavigationRecord", "BeamXYZ88", "XYZ88Datagram", "PointCloud"]
