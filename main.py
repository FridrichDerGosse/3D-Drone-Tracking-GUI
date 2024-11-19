"""
main.py
14. November 2024

<description>

Author:
Nilusink
"""
from gui.tools import Vec2, Vec3, CombinedResult, AngularTrack, TrackUpdate
from gui.camera import CameraConfig
from gui.viewer import Viewer
import math as m
from gui.tools import Track, Box


CAMERAS = [
    CameraConfig(
        0,
        Vec3.from_polar(0, .02, 10),# + Vec3.from_cartesian(0, 0, .3),
        -Vec3.from_polar(0, -.1, 10),
        Vec2.from_cartesian(.88888888, .5),
        Vec2.from_cartesian(1920, 1080)
    ),
    CameraConfig(
        1,
        Vec3.from_polar((2*m.pi) / 3, .02, 10),# + Vec3.from_cartesian(0, 0, .3),
        -Vec3.from_polar((2*m.pi) / 3, -.1, 10),
        Vec2.from_cartesian(.88888888, .5),
        Vec2.from_cartesian(1920, 1080)
    ),
    CameraConfig(
        2,
        Vec3.from_polar((4*m.pi) / 3, .02, 10),#+ Vec3.from_cartesian(0, 0, .3),
        -Vec3.from_polar((4*m.pi) / 3, -.1, 10),
        Vec2.from_cartesian(.88888888, .5),
        Vec2.from_cartesian(1920, 1080)
    )
]


# t1 = Track(Box(Vec2.from_cartesian(1200, 540), Vec2.from_cartesian(0, 0)))
# t2 = Track(Box(Vec2.from_cartesian(720, 530), Vec2.from_cartesian(0, 0)))
# t3 = Track(Box(Vec2.from_cartesian(1200, 540), Vec2.from_cartesian(0, 0)))

# create a singular track


v = Viewer(cameras=CAMERAS)

i = 0
while True:
    i += 1
    v.step()

    track = CombinedResult(
        [
            AngularTrack(0, Vec3.from_polar((500 -i) / 800, i / 1000, 1)),
            AngularTrack(1, Vec3.from_polar((500 -i) / 800, i / 1000, 1)),
            AngularTrack(2, Vec3.from_polar((500 -i) / 800, i / 1000, 1)),
        ],
        TrackUpdate(0, Vec3(), 1)
    )
    v.update_tracks([track])

    if i > 1500:
        i = 0
