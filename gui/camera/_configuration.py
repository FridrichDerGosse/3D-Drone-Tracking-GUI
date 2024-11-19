"""
_configuration.py
14. November 2024

Defines a camera and its properties

Author:
Nilusink
"""
from dataclasses import dataclass
from ..tools import Vec2, Vec3


@dataclass(frozen=True)
class CameraConfig:
    position: Vec3
    direction: Vec3
    fov: Vec2  # in rad
    resolution: Vec2
