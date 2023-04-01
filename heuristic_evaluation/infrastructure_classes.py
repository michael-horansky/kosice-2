"""
created on: 2023-04-01
author:     michal horansky
----------------------------
classfile for HackKosice 2023
road: represents a road, a walkway, a cycle path, a bus connection etc
intersection: lightweight class that represents an intersection in the
    graph representation of infrastructure
bulding: represents a building or a facility
----------------------------
This software is distributed under the GNU General Public License (GPL-3.0-or-later).
It may be used, modified, shared, or built upon.
All derivative work must be distributed under the same license.
"""


# a list of the modes of transportation the model considers
modes_of_transportation = ['walk', 'cycle', 'car']

# a list of building types
building_types = ['residential', 'convenience', 'pharmacy', 'jozko vajda']

class Road():
    
    # ---------------- constructors, destructors, descriptors ----------------------
    
    def __init__(self, connected_intersections, transportation_lengths = {}):
        self.connected_intersections = connected_intersections
        
        self.lengths = transportation_lengths


class Intersection():
    
    # ---------------- constructors, destructors, descriptors ----------------------
    
    def __init__(self, location):
        # location is always a list [longitude, latitude]
        self.location = location
        
        self.roads = []
    
    # ---------------------- parameter-access functions ----------------------------
    
    def add_road(self, road):
        self.roads.append(road)


class Building():
    
    # ---------------- constructors, destructors, descriptors ----------------------
    
    def __init__(self, location, service, surface_area, parameters):
        # 'service' encodes what type of building this is
        # 'residential', 'grocery', 'pharmacy'...
        # 'parameters' is a list of parameters specific to that specific building type
        
        self.location = location
        self.service = service
        self.surface_area = surface_area
        self.parameters = parameters

    
