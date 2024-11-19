"""
_environment.py
14. November 2024

<description>

Author:
Nilusink
"""
from ursina import Ursina, EditorCamera, window, Entity
from ursina.shaders import lit_with_shadows_shader
from ursina.color import rgb32
from ursina import Sky
import typing as tp

from ..tools import Track
from ..tools import Vec3
from ..camera import CameraConfig
from ._camera import Camera
from ._shapes import line


class Viewer:
    _cameras: list[Camera]

    def __init__(
            self,
            cameras: tp.Iterable[CameraConfig],
    ) -> None:
        self._cameras = []
        self.ursina = Ursina()
        window.color = (0, 0, 0, 0)

        # floor
        Entity(
            model='plane',
            scale=50,
            color=rgb32(2, 179, 2),
            shader=lit_with_shadows_shader,
            position=(0, 0, -.2)
        )

        # light
        Sky(color=rgb32(155, 155, 155), shader=lit_with_shadows_shader)

        # cameras
        for cam in cameras:
            self._cameras.append(Camera(cam))

        line(Vec3(), Vec3.from_cartesian(1, 0, 0), color=rgb32(255, 0, 0), thickness=3)
        line(Vec3(), Vec3.from_cartesian(0, 1, 0), color=rgb32(0, 255, 0), thickness=4)
        line(Vec3(), Vec3.from_cartesian(0, 0, 1), color=rgb32(0, 0, 255), thickness=1)

        EditorCamera()  # add camera controls for orbiting and moving the camera

    def step(self) -> None:
        self.ursina.step()

    def update_tracks(self, tracks: tuple[tp.Iterable[Track], ...]) -> None:
        """
        :param tracks: structure: ([tracks per camera], [tracks per other camera])
        """
        for i, cam_tracks in enumerate(tracks):
            self._cameras[i].update_tracks(cam_tracks)
