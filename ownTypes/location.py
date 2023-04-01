from dataclasses import dataclass
import numpy as np

earth_radius = 6.371e06

@dataclass
class Location:
    lon: float
    lat: float

    @property
    def pair(self) -> tuple[float, float]:
        return (self.lon, self.lat)
    
    def distance(self, loc):
        # distance from other location
        lon2, lat2 = loc.pair
        delta_lon = np.deg2rad(self.lon - lon2)
        delta_lat = np.deg2rad(self.lat - lat2)
        delta_x_sq = delta_lon * delta_lon * earth_radius * earth_radius * np.sin(np.deg2rad(self.lon)) * np.sin(np.deg2rad(self.lon))
        delta_y_sq = delta_lat * delta_lat * earth_radius * earth_radius
        return(np.sqrt(delta_x_sq + delta_y_sq))
