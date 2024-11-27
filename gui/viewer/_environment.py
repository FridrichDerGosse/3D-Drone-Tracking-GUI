"""
_environment.py
14. November 2024

<description>

Author:
Nilusink
"""
from ursina import Ursina, EditorCamera, window, Entity
from ursina.shaders import lit_with_shadows_shader
from concurrent.futures import ThreadPoolExecutor
from ursina.color import rgb32
from ursina import Sky
import typing as tp

from ..tools import Vec3, AngularTrack, Track, Vec2, debugger, SimpleLock, run_with_debug
from ..tools.comms import TRes3Data, SInfData, CamAngle3
from ..camera import CameraConfig
from ._camera import Camera
from ._track import Track3D
from ._shapes import line


class Viewer:
    _cameras: dict[int, Camera]

    def __init__(
            self,
            cameras: tp.Iterable[CameraConfig],
            pool: ThreadPoolExecutor
    ) -> None:
        self._cameras = {}
        self._tracks: dict[int, Track3D] = {}
        self._pool = pool
        self.ursina = Ursina()
        window.color = (0, 0, 0, 0)

        # floor
        Entity(
            model='plane',
            scale=50,
            # color=rgb32(2, 179, 2),
            color=rgb32(100, 140, 111),
            shader=lit_with_shadows_shader,
            position=(0, -.2, 0)
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

        # threading stuff
        self._thread_update_lock = SimpleLock()

    def step(self) -> None:
        self.ursina.step()

    # @run_with_debug(show_args=True)
    def update_cam(self, cam: SInfData) -> None:
        """
        update camera information
        """
        # convert message to correct data types
        cconfig = CameraConfig(
            cam.id,
            Vec3.from_cartesian(*cam.position),
            Vec3.from_cartesian(*cam.direction),
            Vec2.from_cartesian(*cam.fov),
            Vec2.from_cartesian(*cam.resolution)
        )

        # if camera doesn't exist, create it
        if cam.id not in self._cameras:
            self._cameras[cam.id] = Camera(cconfig)
            return

        # if camera does exist, update it
        self._cameras[cam.id].update(cconfig)

    @run_with_debug(show_args=True)
    def update_track(self, track: TRes3Data) -> None:
        """
        update a 3d track
        """
        debugger.log("track update")

        # make sure that no two tracks are updated at the same time
        self._thread_update_lock.acquire()

        # update 3d tracks
        tid = track.track_id
        if tid not in self._tracks:
            self._tracks[tid] = Track3D(
                Track(
                    tid,
                    Vec3.from_cartesian(*track.position),
                    track.track_type
                )
            )

        self._tracks[tid].update_track(
            Vec3.from_cartesian(*track.position),
            track.track_type
        )

        # update cameras
        # a1 = CamAngle3(cam_id=0, position=(10.0, 0.0, 0.0),
        #                direction=(-0.9761160908245395, -0.02929227093332195, 0.21526574297130507))
        # a2 = CamAngle3(cam_id=1, position=(-4.999999999999998, 8.660254037844387, 0.0),
        #                direction=(0.5689841315221609, -0.790963239543564, 0.22502046966159106))
        # a3 = CamAngle3(cam_id=2, position=(-5.000000000000004, -8.660254037844386, 0.0),
        #                direction=(0.424894616238502, 0.8498929878596323, 0.3116832916255907))
        #
        # angles = [AngularTrack(
        #     a.cam_id,
        #     Vec3.from_cartesian(*a.position),
        #     Vec3.from_cartesian(*a.direction) * 3
        # ) for a in [a1, a2, a3]]

        # return
        for angle in track.cam_angles:
            debugger.trace(f"updating cam")
            if angle.cam_id in self._cameras:
                # self._pool.submit(self._cameras[angle.cam_id].update_tracks, [angle])
                self._pool.submit(
                    self._cameras[angle.cam_id].update_tracks,
                    [AngularTrack(
                        angle.cam_id,
                        Vec3.from_cartesian(*angle.position),
                        Vec3.from_cartesian(*angle.direction))
                    ]
                )

        self._thread_update_lock.release()
