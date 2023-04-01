from dataclasses import dataclass


@dataclass
class Location:
    x: float
    y: float

    @property
    def lat(self) -> float:
        return self.x

    @property
    def lon(self) -> float:
        return self.y

    @property
    def pair(self) -> tuple[float, float]:
        return (self.x, self.y)
