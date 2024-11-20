"""
_track.py
20. November 2024

3d Visualization of a track

Author:
Nilusink
"""
from ursina import Entity, Vec3 as UVec3
from ursina.color import rgb32, Color

from ..tools import Track, Vec3


TRACK_TYPE_COLORMAP: dict[int, Color] = {
    -1: rgb32(140, 78, 76),  # degraded
    0: rgb32(95, 150, 245),  # new
    1: rgb32(13, 217, 69)    # valid
}


class Track3D(Entity):
    def __init__(self, track: Track) -> None:
        self._track = track

        super().__init__(
            model="sphere",
            position=UVec3(),
            scale=.1,
            color=TRACK_TYPE_COLORMAP[track.track_type]
        )

        # proper position (y and z flipped)
        self.position = track.position

    def update_track(
            self,
            pos: Vec3,
            track_type: int | None = None
    ) -> None:
        self._track.update_track(pos, track_type)

    @property
    def position(self) -> Vec3:
        p = self.position
        return Vec3.from_cartesian(p.x, p.z, p.y)

    @position.setter
    def position(self, value: Vec3) -> None:
        super().position_setter(UVec3(value.x, value.z, value.y))

    def update(self) -> None:
        self.position = self._track.position
        self.color_setter(TRACK_TYPE_COLORMAP[self._track.track_type])
