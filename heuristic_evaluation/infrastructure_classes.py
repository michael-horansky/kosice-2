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
from ownTypes.location import Location

modes_of_transportation = ["walk", "cycle", "car"]

# a list of building types
building_types = ["residential", "convenience", "pharmacy", "jozko vajda"]


class CityObject:

    # ---------------- constructors, destructors, descriptors ----------------------

    def __init__(self, parent_city_model):
        self.parent_city_model = parent_city_model

    def __str__(self):
        return f"City object at {self.parent_city_model.city_name}"


class Road(CityObject):

    # ---------------- constructors, destructors, descriptors ----------------------

    def __init__(
        self, parent_city_model, connected_intersections, transportation_lengths={}
    ):
        super(Road, self).__init__(parent_city_model)
        self.connected_intersections = connected_intersections

        self.lengths = transportation_lengths

    def __str__(self):
        return f"Road at {self.parent_city_model.city_name} connecting positions {'; '.join([str(intersection.location) for intersection in self.connected_intersections])}"


class Intersection(CityObject):

    location: Location
    roads: list[Road]

    # ---------------- constructors, destructors, descriptors ----------------------

    def __init__(self, location: Location):
        self.location = location
        self.roads = []

    # ---------------------- parameter-access functions ----------------------------

    def add_road(self, road: Road):
        self.roads.append(road)


class Building(CityObject):

    # ---------------- constructors, destructors, descriptors ----------------------

    def __init__(self, location: Location, service, surface_area, parameters):
        # 'service' encodes what type of building this is
        # 'residential', 'grocery', 'pharmacy'...
        # 'parameters' is a list of parameters specific to that specific building type

        self.location = location
        self.service = service
        self.surface_area = surface_area
        self.parameters = parameters

