"""
main.py
14. November 2024

<description>

Author:
Nilusink
"""
from gui.camera import CameraConfig
from gui.tools import Vec2, Vec3
from gui.viewer import Viewer
import math as m
from gui.tools import Track, Box


CAMERAS = [
    CameraConfig(
        Vec3.from_polar(0, .02, 10),# + Vec3.from_cartesian(0, 0, .3),
        -Vec3.from_polar(0, -.1, 10),
        Vec2.from_cartesian(.88888888, .5),
        Vec2.from_cartesian(1920, 1080)
    ),
    CameraConfig(
        Vec3.from_polar((2*m.pi) / 3, .02, 10),# + Vec3.from_cartesian(0, 0, .3),
        -Vec3.from_polar((2*m.pi) / 3, -.1, 10),
        Vec2.from_cartesian(.88888888, .5),
        Vec2.from_cartesian(1920, 1080)
    ),
    CameraConfig(
        Vec3.from_polar((4*m.pi) / 3, .02, 10),#+ Vec3.from_cartesian(0, 0, .3),
        -Vec3.from_polar((4*m.pi) / 3, -.1, 10),
        Vec2.from_cartesian(.88888888, .5),
        Vec2.from_cartesian(1920, 1080)
    )
]


t1 = Track(Box(Vec2.from_cartesian(1200, 540), Vec2.from_cartesian(0, 0)))
t2 = Track(Box(Vec2.from_cartesian(720, 530), Vec2.from_cartesian(0, 0)))
t3 = Track(Box(Vec2.from_cartesian(1200, 540), Vec2.from_cartesian(0, 0)))


v = Viewer(cameras=CAMERAS)

while True:
    v.step()
    v.update_tracks(((t1,), (t2,), (t3,)))
