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
    
    @property
    def absolute_position(self):
        x = np.cos(np.deg2rad(self.lon)) * np.cos(np.deg2rad(self.lat)) * earth_radius
        y = np.sin(np.deg2rad(self.lon)) * np.cos(np.deg2rad(self.lat)) * earth_radius
        z = np.sin(np.deg2rad(self.lat)) * earth_radius
        return (x, y, z)
    
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
    
    def distance_from_great_arc(self, loc1, loc2):
        # smallest distance between self and a great arc given by loc1 and loc2
        x, y, z = self.absolute_position
        x1, y1, z1 = loc1.absolute_position
        x2, y2, z2 = loc2.absolute_position
        Q_cross_R_x = y1 * z2 - y2 * z1
        Q_cross_R_y = z1 * x2 - z2 * x1
        Q_cross_R_z = x1 * y2 - x2 * y1
        # normalize the displacement vector
        size_Q_cross_R = np.sqrt(Q_cross_R_x * Q_cross_R_x + Q_cross_R_y * Q_cross_R_y + Q_cross_R_z * Q_cross_R_z)
        Q_cross_R_x /= size_Q_cross_R
        Q_cross_R_y /= size_Q_cross_R
        Q_cross_R_z /= size_Q_cross_R
        
        P_dot_Q_cross_R = x * Q_cross_R_x + y * Q_cross_R_y + z * Q_cross_R_z
        pos_on_road_x = x - P_dot_Q_cross_R * Q_cross_R_x
        pos_on_road_y = y - P_dot_Q_cross_R * Q_cross_R_y
        pos_on_road_z = z - P_dot_Q_cross_R * Q_cross_R_z
        distance_along_road = np.sqrt((x1 - pos_on_road_x) * (x1 - pos_on_road_x) + (y1 - pos_on_road_y) * (y1 - pos_on_road_y) + (z1 - pos_on_road_z) * (z1 - pos_on_road_z))
        return(P_dot_Q_cross_R, distance_along_road) # also return the distance along the arc mate
    
    def distance_from_road(self, road):
        distance_from_road_arc, distance_along_road = self.distance_from_great_arc(road.connected_intersections[0].location, road.connected_intersections[1].location)
        distance_from_first_intersection = self.distance(road.connected_intersections[0].location)
        distance_from_second_intersection = self.distance(road.connected_intersections[1].location)
        if distance_from_first_intersection < distance_from_road_arc and distance_from_first_intersection < distance_from_second_intersection:
            return (distance_from_first_intersection, 0.0)
        elif distance_from_second_intersection < distance_from_road_arc and distance_from_second_intersection < distance_from_first_intersection:
            return (distance_from_second_intersection, road.physical_length)
        else:
            return(distance_from_road_arc, distance_along_road)
        
        
        
