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
        #for intersection in intersections:
        #    intersection.add_road(new_road)

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
    
    def shortest_path_between_intersections(self, start_intersection, end_intersection, mode_of_transportation):
        
        def get_neighbour(intersection, road):
            if road.connected_intersections[0] == intersection:
                return(road.connected_intersections[1])
            else:
                return(road.connected_intersections[0])
        
        # d-d-d-dijkstra
        unvisited_nodes = self.intersections.copy()
        tentative_distances = {start_intersection : 0.0}
        current_node = start_intersection
        while(True):
            if current_node == end_intersection:
                return(tentative_distances[current_node])
            for i in range(len(current_node.roads)):
                target_node = get_neighbour(current_node, current_node.roads[i])
                new_tentative_dist = tentative_distances[current_node] + current_node.roads[i].physical_length / current_node.roads[i].speeds[mode_of_transportation]
                if target_node in tentative_distances.keys():
                    if tentative_distances[target_node] < new_tentative_dist:
                        continue
                tentative_distances[target_node] = new_tentative_dist
            unvisited_nodes.remove(current_node)
            
            first_considered_index = 0
            current_smallest_unvisited_tentative_distance = -1
            current_closest_node = -1
            success = False
            while(first_considered_index < len(tentative_distances.keys())):
                considered_node = list(tentative_distances.keys())[first_considered_index]
                first_considered_index += 1
                if considered_node in unvisited_nodes:
                    success = True
                    current_smallest_unvisited_tentative_distance = tentative_distances[considered_node]
                    current_closest_node = considered_node
                    break
            if success == False:
                # no more unvisited marked nodes left - no path exists
                print("No path between the two nodes exists")
                return(-1)
            for i in range(first_considered_index, len(tentative_distances.keys())):
                considered_node = list(tentative_distances.keys())[i]
                if considered_node in unvisited_nodes and tentative_distances[considered_node] < current_smallest_unvisited_tentative_distance:
                    current_smallest_unvisited_tentative_distance = tentative_distances[considered_node]
                    current_closest_node = considered_node
            current_node = current_closest_node
        
                    
            
            
            
        
