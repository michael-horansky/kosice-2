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

def N_max_elements(list1, N, eval_function = lambda x: x): 
    final_list = [] 
  
    for i in range(0, N): 
        max1 = eval_function(list1[0])
        index1 = 0
          
        for j in range(1, len(list1)):
            if eval_function(list1[j]) > max1: 
                max1 = eval_function(list1[j])
                index1 = j
                  
        final_list.append(list1.pop(index1)) 
          
    return(final_list)

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
        #N_closest_intersections_checked = 3
        #closest_intersections = N_max_elements(self.intersections, N_closest_intersections_checked, eval_function = lambda x: )
        closest_road = N_max_elements(self.roads, 1, eval_function = lambda x: - start_location.distance_from_road(x)[0])
        print(closest_road)
