"""
test_main.py
14. November 2024

<description>

Author:
Nilusink
"""
from gui.tools import Vec2, Vec3, CombinedResult, AngularTrack, TrackUpdate
from gui.camera import CameraConfig
from gui.viewer import Viewer
import math as m


# initial configuration for demo (will be automated)
CAMERAS = [
    CameraConfig(
        id=0,
        position=Vec3.from_polar(0, .02, 10),# + Vec3.from_cartesian(0, 0, .3),
        direction=-Vec3.from_polar(0, -.1, 10),
        fov=Vec2.from_cartesian(.88888888, .5),
        resolution=Vec2.from_cartesian(1920, 1080)
    ),
    CameraConfig(
        id=1,
        position=Vec3.from_polar((2*m.pi) / 3, .02, 10),# + Vec3.from_cartesian(0, 0, .3),
        direction=-Vec3.from_polar((2*m.pi) / 3, -.1, 10),
        fov=Vec2.from_cartesian(.88888888, .5),
        resolution=Vec2.from_cartesian(1920, 1080)
    ),
    CameraConfig(
        id=2,
        position=Vec3.from_polar((4*m.pi) / 3, .02, 10),#+ Vec3.from_cartesian(0, 0, .3),
        direction=-Vec3.from_polar((4*m.pi) / 3, -.1, 10),
        fov=Vec2.from_cartesian(.88888888, .5),
        resolution=Vec2.from_cartesian(1920, 1080)
    )
]


v = Viewer(cameras=CAMERAS)

# demo
i = 0
while True:
    i += 1
    v.step()

    cam_results = [
        AngularTrack(0, Vec3.from_polar((500 -i) / 800, i / 1000, 1)),
        AngularTrack(1, Vec3.from_polar((500 -i) / 800, i / 1000, 1)),
        AngularTrack(2, Vec3.from_polar((500 -i) / 800, i / 1000, 1)),
    ]

    track = CombinedResult(
        cam_results,
        TrackUpdate(
            track_id=0,
            pos=Vec3(),
            track_type=1
        )
    )
    v.update_tracks([track])

    if i > 1500:
        i = 0
