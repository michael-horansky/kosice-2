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

from .infrastructure_classes import Building, Intersection, Road, building_types, default_transportation_speeds

default_service_weights = {'children_clinic' : 2, 'post_office' : 2.5, 'dental_clinic' : 2, 'restaurant' : 3, 'playground' : 3, 'supermarket' : 5,
                           'elementary_school' : 4, 'dog_enclosure' : 0, 'drug_store' : 3, 'parcel_locker' : 1, 'bus_stop' : 4, 'kindergarten' : 2, 'fitness' : 3,
                           'bar' : 1, 'pub' : 2, 'fast_food' : 0, 'pharmacy' : 4, 'convenience' : 2, 'cafe' : 0, 'general_clinic' : 3, 'UNCATEGORIZED' : 0}

def N_max_elements(list1, N, eval_function = lambda x: x):
    init_list = list1.copy()
    final_list = [] 
  
    for i in range(0, N): 
        max1 = eval_function(init_list[0])
        index1 = 0
          
        for j in range(1, len(init_list)):
            if eval_function(init_list[j]) > max1: 
                max1 = eval_function(init_list[j])
                index1 = j
                  
        final_list.append(init_list.pop(index1)) 
          
    return(final_list)

class CityModel:

    #buildings: list[Building]

    # ---------------- constructors, destructors, descriptors ----------------------

    def __init__(self, city_name="Kosice", direct_path_treshold = 20.0, largest_interesting_time_distance = 25.0 * 60.0):

        self.intersections = []
        self.roads = []
        self.buildings = []
        self.buildings_by_type = {service: [] for service in building_types}

        self.city_name = "Kosice"
        self.direct_path_treshold = direct_path_treshold #if a distance between two locations is smaller than this, you can leg it directly
        self.largest_interesting_time_distance = largest_interesting_time_distance # if a distance is bigger than this, just forget it

    def __str__(self):
        return ""

    # ---------------------- parameter-access functions ----------------------------

    def add_intersection(self, new_intersection):

        self.intersections.append(new_intersection)

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
        # returns a tuple (nearest_road, distance to nearest road, distance along the road from its first connected intersection)
        #N_closest_intersections_checked = 3
        #closest_intersections = N_max_elements(self.intersections, N_closest_intersections_checked, eval_function = lambda x: )
        nearest_road = N_max_elements(self.roads, 1, eval_function = lambda x: - start_location.distance_from_road(x)[0])[0]
        return(nearest_road, *start_location.distance_from_road(nearest_road))
    
    def shortest_path_between_intersections(self, start_intersection, end_intersections, mode_of_transportation):
        
        def get_neighbour(intersection, road):
            if road.connected_intersections[0] == intersection:
                return(road.connected_intersections[1])
            else:
                return(road.connected_intersections[0])
        
        # d-d-d-dijkstra
        if type(end_intersections) != list:
            end_intersections = [end_intersections]
        unvisited_end_intersections = end_intersections.copy()
        end_intersections_distances = {}
        
        unvisited_nodes = self.intersections.copy()
        tentative_distances = {start_intersection : 0.0}
        current_node = start_intersection
        while(True):
            if current_node in unvisited_end_intersections:
                unvisited_end_intersections.remove(current_node)
                end_intersections_distances[current_node] = tentative_distances[current_node]
                if len(unvisited_end_intersections) <= 0:
                    return(end_intersections_distances)
                #return(tentative_distances[current_node])
            for i in range(len(current_node.roads)):
                # check if road is traversable with this mode of transportation
                if current_node.roads[i].speeds[mode_of_transportation] == -1:
                    continue
                target_node = get_neighbour(current_node, current_node.roads[i])
                new_tentative_dist = tentative_distances[current_node] + current_node.roads[i].physical_length / current_node.roads[i].speeds[mode_of_transportation]
                # a distance bigger than a certain number is treated as infinity
                if new_tentative_dist > self.largest_interesting_time_distance:
                    continue
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
    
    def find_path_between_two_locations(self, start_location, end_location, mode_of_transportation, walk_speed = default_transportation_speeds['walk']):
        # check if you should just leg it, mate
        if start_location.distance(end_location) < self.direct_path_treshold:
            return(start_location.distance(end_location))
        start_nearest_road, start_distance_to_road, start_road_offset = self.find_distance_to_nearest_road(start_location)
        end_nearest_road  , end_distance_to_road  , end_road_offset   = self.find_distance_to_nearest_road(end_location  )
        
        distances_from_first_start_intersection = self.shortest_path_between_intersections(
            start_nearest_road.connected_intersections[0], end_nearest_road.connected_intersections, mode_of_transportation)
        distances_from_second_start_intersection = self.shortest_path_between_intersections(
            start_nearest_road.connected_intersections[1], end_nearest_road.connected_intersections, mode_of_transportation)
        walking_part = (start_distance_to_road + end_distance_to_road) / walk_speed
        d1_1 = walking_part + (start_road_offset / start_nearest_road.speeds[mode_of_transportation]) + (end_road_offset / end_nearest_road.speeds[mode_of_transportation]) + distances_from_first_start_intersection[end_nearest_road.connected_intersections[0]]
        d1_2 = walking_part + (start_road_offset / start_nearest_road.speeds[mode_of_transportation]) + ((end_nearest_road.physical_length - end_road_offset) / end_nearest_road.speeds[mode_of_transportation]) + distances_from_first_start_intersection[end_nearest_road.connected_intersections[1]]
        d2_1 = walking_part + ((start_nearest_road.physical_length - start_road_offset) / start_nearest_road.speeds[mode_of_transportation]) + (end_road_offset / end_nearest_road.speeds[mode_of_transportation]) + distances_from_second_start_intersection[end_nearest_road.connected_intersections[0]]
        d2_2 = walking_part + ((start_nearest_road.physical_length - start_road_offset) / start_nearest_road.speeds[mode_of_transportation]) + ((end_nearest_road.physical_length - end_road_offset) / end_nearest_road.speeds[mode_of_transportation]) + distances_from_second_start_intersection[end_nearest_road.connected_intersections[1]]
        
        return(min([d1_1, d1_2, d2_1, d2_2]))
    
    def find_score_of_location(self, start_location, service_weights = default_service_weights):
        print("si sa ojebal")
        
        
                    
            
            
            
        
