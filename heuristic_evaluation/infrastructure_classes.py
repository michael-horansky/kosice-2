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
from typing import List, Optional

from ownTypes.location import Location

modes_of_transportation = ["walk", "cycle", "car"]

# a list of building types
default_service_weights = {
    "children_clinic": 2,
    "post_office": 2.5,
    "dental_clinic": 2,
    "restaurant": 3,
    "playground": 3,
    "supermarket": 5,
    "elementary_school": 4,
    "dog_enclosure": 0,
    "drug_store": 3,
    "parcel_locker": 1,
    "bus_stop": 4,
    "kindergarten": 2,
    "fitness": 3,
    "bar": 1,
    "pub": 2,
    "fast_food": 0,
    "pharmacy": 4,
    "convenience": 2,
    "cafe": 0,
    "general_clinic": 3,
    "UNCATEGORIZED": 0,
}
building_types = list(default_service_weights.keys())[:-1] + [
    "residential"
]  # ["residential", "convenience", "pharmacy", "jozko vajda"]

default_transportation_speeds = {"walk": 1.0, "bike": 6.0, "car": 10.0}  # in m/s


class CityObject:

    # ---------------- constructors, destructors, descriptors ----------------------

    def __init__(self, parent_city_model):
        self.parent_city_model = parent_city_model

    def __str__(self):
        return f"City object at {self.parent_city_model.city_name}"


class Intersection(CityObject):

    id: Optional[int]

    """
    location: Location
    roads: list[Road]
    """
    # ---------------- constructors, destructors, descriptors ----------------------

    def __init__(self, location: Location):
        self.location = location
        self.roads = []
        self.id = None

    # ---------------------- parameter-access functions ----------------------------

    def add_road(self, road):
        self.roads.append(road)

    def setId(self, id: int) -> None:
        self.id = id


class Road(CityObject):

    connected_intersections: List[Intersection]

    # ---------------- constructors, destructors, descriptors ----------------------

    def __init__(
        self,
        parent_city_model,
        connected_intersections,
        transportation_speeds=default_transportation_speeds,
    ):
        super(Road, self).__init__(parent_city_model)
        self.connected_intersections = connected_intersections

        for intersection in self.connected_intersections:
            intersection.add_road(self)

        self.speeds = transportation_speeds

    def __str__(self):
        return f"Road at {self.parent_city_model.city_name} connecting positions {'; '.join([str(intersection.location) for intersection in self.connected_intersections])}"

    def __repr__(self):
        return self.__str__()

    @property
    def physical_length(self):
        return self.connected_intersections[0].location.distance(
            self.connected_intersections[1].location
        )


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

