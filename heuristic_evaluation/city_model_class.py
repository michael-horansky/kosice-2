"""
created on: 2023-04-01
author:     michal horansky
----------------------------
classfile for HackKosice 2023
city_model: encodes the abstract city map model, provides heuristic evaluators for relevant
    parameters
----------------------------
This software is distributed under the GNU General Public License (GPL-3.0-or-later).
It may be used, modified, shared, or built upon.
All derivative work must be distributed under the same license.
"""

from ownTypes.location import Location

from .infrastructure_classes import Building, Intersection, Road, building_types


class CityModel:

    #buildings: list[Building]

    # ---------------- constructors, destructors, descriptors ----------------------

    def __init__(self, city_name="Kosice"):

        self.intersections = []
        self.roads = []
        self.buildings = []
        self.buildings_by_type = {service: [] for service in building_types}

        self.city_name = "Kosice"

    def __str__(self):
        return ""

    # ---------------------- parameter-access functions ----------------------------

    def add_intersection(self, position: Location):

        self.intersections.append(Intersection(position))

    def add_road(self, intersections):
        new_road = Road(self, intersections)
        self.roads.append(new_road)
        for intersection in intersections:
            intersection.add_road(new_road)

    def add_building(self, building):
        self.buildings.append(building)
        try:
            self.buildings_by_type[building.service].append(building)
            return self
        except KeyError:
            print("building service not recognised")
            return -1

    # ------------------------ path-finding functions ------------------------------
    
    def find_distance_to_nearest_road(self, start_location):
        # returns a tuple (distance to nearest road, nearest_road, distance along the road from its first connected intersection)
        N_closest_intersections_checked = 3
