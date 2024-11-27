"""
_camera.py
14. November 2024

<description>

Author:
Nilusink
"""
from ursina.shaders import lit_with_shadows_shader
from ursina import Vec3 as UVec3
from ursina import *
import typing as tp
import math as m

from ..tools import AngularTrack, Vec3, debugger, run_with_debug
from ..camera import CameraConfig
from ._shapes import line

model = load_model('assets/turret')


class Camera(Entity):
    distance: int = 10
    _last_track_entities: list[Entity]
    _id: int

    @run_with_debug(reraise_errors=True)
    def __init__(self, config: CameraConfig, scale: float = 1) -> None:
        self._config = config
        self._last_track_entities = []

        super().__init__(
            model='assets/turret',
            # model=model.copy(),
            # model="cube",
            position=UVec3(),
            scale=scale,
            # texture="assets/Tesla-Cybertruck-Metro-Look.jpg",
            shader=lit_with_shadows_shader
        )
        self.position = config.position
        self.rotation_y = (-config.direction.angle_xy * (180 / m.pi)) + 180

        self._lines: list[Entity] = []
        self._draw_fov_lines()

    @property
    def position(self) -> Vec3:
        p = self._config.position
        return Vec3.from_cartesian(p.x, p.z, p.y)

    @position.setter
    def position(self, value: Vec3) -> None:
        super().position_setter(UVec3(value.x, value.z, value.y))

    @property
    def config(self) -> CameraConfig:
        return self._config

    @config.setter
    def config(self, value: CameraConfig) -> None:
        # update position and rotation
        self.position = value.position
        self.rotation_y = (-value.direction.angle_xy * (180 / m.pi)) + 180

        # check if fov has been updated
        if self._config.fov.xy != value.fov.xy:
            self._draw_fov_lines()

        # update config
        self._config = value

    @property
    def id(self) -> int:
        return self._config.id

    def _draw_fov_lines(self) -> None:
        """
        draw fov visualisation
        """
        for l in self._lines:
            destroy(l)

        self._lines.clear()

        # create "cone" in front of camera
        l1 = self._config.direction.copy()
        l1.angle_xy += self._config.fov.x / 2
        l1.angle_xz += self._config.fov.y / 2
        l1.length = self.distance
        l1 += self._config.position

        l2 = self._config.direction.copy()
        l2.angle_xy += self._config.fov.x / 2
        l2.angle_xz -= self._config.fov.y / 2
        l2.length = self.distance
        l2 += self._config.position

        l3 = self._config.direction.copy()
        l3.angle_xy -= self._config.fov.x / 2
        l3.angle_xz += self._config.fov.y / 2
        l3.length = self.distance
        l3 += self._config.position

        l4 = self._config.direction.copy()
        l4.angle_xy -= self._config.fov.x / 2
        l4.angle_xz -= self._config.fov.y / 2
        l4.length = self.distance
        l4 += self._config.position

        # forward lines
        self._lines.append(line(self._config.position, l1))
        self._lines.append(line(self._config.position, l2))
        self._lines.append(line(self._config.position, l3))
        self._lines.append(line(self._config.position, l4))

        # closing lines
        self._lines.append(line(l1, l2, l4, l3, close=True))

    # @run_with_debug(show_finish=True, reraise_errors=True)
    def update_tracks(self, tracks: tp.Iterable[AngularTrack]) -> None:
        debugger.trace(f"updating camera tracks: {len(tracks)}")
        # delete old entities
        for e in self._last_track_entities:
            destroy(e)

        # assign to temporary variables for better readability
        # px, py = self.config.resolution.xy
        # fx, fy = self.config.fov.xy

        for track in tracks:
            debugger.trace(f"updating camera track: {track.cam_id}")
            # x, y = track.last_box.center.xy
            #
            # # cast to 3d direction
            # angle_xy = -((x - px / 2) / px) * fx
            # angle_xz = -((y - py / 2) / py) * fy
            #
            # trace = Vec3.from_polar(angle_xy, angle_xz, 1)
            # trace.angle_xz += self.config.direction.angle_xz
            # trace.angle_xy += self.config.direction.angle_xy
            trace = track.position + track.direction

            debugger.trace(f"trace calc: {trace.xyz} from {track.direction.xyz}")

            # trace.length = self.distance * 2
            debugger.trace(f"line: {self._config.position.xyz} - {trace.xyz}")

            self._last_track_entities.append(
                line(self._config.position, trace, color=rgb(255, 0, 0))
            )
            debugger.trace(f"drawn")

    # def update(self, *_, **__) -> None:
    #     self.rotation_y += 1
