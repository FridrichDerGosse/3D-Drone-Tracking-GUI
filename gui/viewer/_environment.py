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

from ..tools import CombinedResult, Vec3, AngularTrack, Track
from ..camera import CameraConfig
from ._camera import Camera
from ._shapes import line


class Viewer:
    _cameras: dict[int, Camera]

    def __init__(
            self,
            cameras: tp.Iterable[CameraConfig],
    ) -> None:
        self._cameras = {}
        self._tracks: dict[int, Track] = {}
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
            self._cameras[cam.id] = Camera(cam)

        line(Vec3(), Vec3.from_cartesian(1, 0, 0), color=rgb32(255, 0, 0), thickness=3)
        line(Vec3(), Vec3.from_cartesian(0, 1, 0), color=rgb32(0, 255, 0), thickness=4)
        line(Vec3(), Vec3.from_cartesian(0, 0, 1), color=rgb32(0, 0, 255), thickness=1)

        EditorCamera()  # add camera controls for orbiting and moving the camera

    def step(self) -> None:
        self.ursina.step()

    def update_tracks(self, tracks: tp.Iterable[CombinedResult]) -> None:
        """
        :param tracks: structure: ([tracks per camera], [tracks per other camera])
        """
        # sort all camera tracks to each camera
        cam_results: dict[int, list[AngularTrack]] = {cid: [] for cid in self._cameras}
        for i, track in enumerate(tracks):
            for cam_angle in track.camera_angles:
                cam_results[cam_angle.cam_id].append(cam_angle)

            # update 3d tracks
            tid = track.track_update.track_id
            if tid in self._tracks:
                self._tracks[tid].update_track(
                    track.track_update.pos,
                    track.track_update.track_type
                )

        # update cameras
        for cid, angles in cam_results.items():
            self._cameras[cid].update_tracks(angles)