"""
_track.py
20. November 2024

3d Visualization of a track

Author:
Nilusink
"""
from ursina import Entity, Vec3 as UVec3, destroy
from ursina.color import rgb32, Color, rgba32

from ..tools import Track, Vec3, debugger, run_with_debug
from ._shapes import line


TRACK_TYPE_COLORMAP: dict[int, Color] = {
    -1: rgb32(140, 78, 76),  # degraded
    0: rgb32(95, 150, 245),  # new
    1: rgb32(13, 217, 69)    # valid
}


class Track3D(Entity):
    max_trace_length: int = 100

    # @run_with_debug(reraise_errors=True)
    def __init__(self, track: Track) -> None:
        self._track = track
        self._traces: list[Entity] = []

        super().__init__(
            model="sphere",
            position=UVec3(),
            scale=.1,
            color=TRACK_TYPE_COLORMAP[track.track_type]
        )

        # proper position (y and z flipped)
        self.position = track.position

        # accuracy ball
        self._acc = Entity(
            model="sphere",
            position=self.get_position(),
            scale=track.accuracy,
            color=rgba32(50, 50, 50, 50)
        )

        debugger.info(f"New Track: {track.id}")

    # @run_with_debug(reraise_errors=True, show_finish=True)
    def update_track(
            self,
            pos: Vec3,
            accuracy: float,
            track_type: int | None = None
    ) -> None:
        self._track.update_track(pos, accuracy, track_type)

        self._traces.insert(0, line(
            self._track.position,
            self._track.position_history[-2],
            color=TRACK_TYPE_COLORMAP[self._track.track_type]
        ))

        while len(self._traces) > self.max_trace_length:
            destroy(self._traces.pop(-1))

        # update accuracy
        debugger.log(f"updating accuracy: {accuracy}")
        self._acc.scale = accuracy * 2
        # self.scale = accuracy * 2

        debugger.log(f"Track {self._track.id} updated")

    @property
    def position(self) -> Vec3:
        p = self._config.position
        return Vec3.from_cartesian(p.x, p.z, p.y)

    @position.setter
    def position(self, value: Vec3) -> None:
        super().position_setter(UVec3(value.x, value.z, value.y))

    def update(self) -> None:
        self.position = self._track.position
        self._acc.position = self.get_position()
        self.color_setter(TRACK_TYPE_COLORMAP[self._track.track_type])
