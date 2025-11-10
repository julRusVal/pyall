"""Lightweight data models for working with decoded Kongsberg .ALL content."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence, Tuple

import numpy as np


@dataclass
class NavigationRecord:
    """Decoded representation of a raw ``P`` (position) datagram."""

    timestamp: datetime
    timestamp_unix: float
    latitude: float
    longitude: float
    quality: float
    speed_over_ground: float
    course_over_ground: float
    heading: float
    descriptor: int
    counter: int
    serial_number: int
    raw_payload: Optional[bytes] = None

    def as_track_tuple(self) -> Tuple[float, float, float]:
        """Return the tuple used throughout legacy code (timestamp, lat, lon)."""

        return (self.timestamp_unix, self.latitude, self.longitude)


@dataclass
class BeamXYZ88:
    """Per-beam information from an ``X`` (XYZ88) datagram."""

    depth: float
    across_track: float
    along_track: float
    detection_window_length: int
    quality_factor: int
    beam_incidence_angle_adjustment: float
    detection_information: int
    realtime_cleaning_information: int
    reflectivity: float


@dataclass
class XYZ88Datagram:
    """
    Container for the full contents of an ``X`` (XYZ88) datagram.

    The optional ``timestamp``, ``latitude`` and ``longitude`` fields are only
    populated once georeferencing has been performed (see :func:`loaddata`).
    """

    record_date: int
    time_seconds: float
    counter: int
    serial_number: int
    heading: float
    sound_speed_at_transducer: float
    transducer_depth: float
    n_beams: int
    n_valid_detections: int
    sample_frequency: float
    scanning_info: int
    spare_fields: Tuple[int, int, int]
    beams: Sequence[BeamXYZ88]
    timestamp: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    etx: Optional[int] = None
    checksum: Optional[int] = None


@dataclass
class PointCloud:
    """Normalized point cloud derived from one or more ``X`` datagrams."""

    eastings: np.ndarray
    northings: np.ndarray
    depths: np.ndarray
    quality: np.ndarray
    ids: np.ndarray

    def __post_init__(self) -> None:
        lengths = {arr.size for arr in (self.eastings, self.northings, self.depths, self.quality, self.ids)}
        if len(lengths) != 1:
            raise ValueError("PointCloud arrays must be the same length")

    @property
    def size(self) -> int:
        return int(self.eastings.size)

    def as_arrays(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return self.eastings, self.northings, self.depths, self.quality, self.ids
