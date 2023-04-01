from dataclasses import dataclass
import numpy as np

earth_radius = 6.371e06

@dataclass
class Location():
    lon: float
    lat: float

    @property
    def pair(self):
        return (self.lon, self.lat)
    
    def distance(self, loc):
        # distance from other location
        lon2, lat2 = loc.pair
        """delta_lon = np.deg2rad(self.lon - lon2)
        delta_lat = np.deg2rad(self.lat - lat2)
        delta_x_sq = delta_lon * delta_lon * earth_radius * earth_radius * np.sin(np.deg2rad(self.lon)) * np.sin(np.deg2rad(self.lon))
        delta_y_sq = delta_lat * delta_lat * earth_radius * earth_radius
        return(np.sqrt(delta_x_sq + delta_y_sq))"""
        lon1rad = np.deg2rad(self.lon)
        lat1rad = np.deg2rad(self.lat)
        lon2rad = np.deg2rad(lon2)
        lat2rad = np.deg2rad(lat2)
        return(np.arccos(np.sin(lat1rad) * np.sin(lat2rad) + np.cos(lat1rad) * np.cos(lat2rad) * np.cos(lon2rad - lon1rad)) * earth_radius)
        
