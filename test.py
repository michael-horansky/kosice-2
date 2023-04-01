from heuristic_evaluation.city_model_class import *


kosice = CityModel()
kosice.add_intersection(Intersection(Location(21.238454903302088, 48.69470206219284))) # OC optima
kosice.add_intersection(Intersection(Location(21.263561595515494, 48.69767209785608))) #kongres hotel
kosice.add_intersection(Intersection(Location(21.24140179948478, 48.68645709734484))) #EMELS
kosice.add_road([kosice.intersections[0], kosice.intersections[1]])
kosice.add_road([kosice.intersections[0], kosice.intersections[2]])

print(kosice.roads[0])
print(kosice.roads[0].physical_length)
print("Distance of kosicka futbalova arena from this road:")
futbal = Location(21.24525555514401, 48.696668121624384)
stl_sun = Location(21.24204026260373, 48.6859001524962)
print(futbal.distance_from_road(kosice.roads[0]))
print(stl_sun.distance_from_road(kosice.roads[1]))
print("--------------------------------------------")
kosice.find_distance_to_nearest_road(futbal)
kosice.find_distance_to_nearest_road(stl_sun)

print("--------------------------------------------")
print(kosice.shortest_path_between_intersections(kosice.intersections[1], kosice.intersections[2], 'walk'))

print("--------------------------------------------")
print(kosice.find_path_between_two_locations(futbal, stl_sun, 'car'))
"""
bepis = CityModel()
bepis.add_intersection(Location(0.0, 0.0))
bepis.add_intersection(Location(1.0, 0.0))
bepis.add_intersection(Location(0.0, 10.0))
bepis.add_intersection(Location(0.3, 0.0))
bepis.add_intersection(Location(0.6, 0.0))

bepis.add_road([bepis.intersections[0], bepis.intersections[2]])
bepis.add_road([bepis.intersections[2], bepis.intersections[1]])
print("BEPIS", bepis.shortest_path_between_intersections(bepis.intersections[0], bepis.intersections[1], 'walk'))

bepis.add_road([bepis.intersections[0], bepis.intersections[3]])
bepis.add_road([bepis.intersections[3], bepis.intersections[4]])
bepis.add_road([bepis.intersections[4], bepis.intersections[1]])
print("BEPIS", bepis.shortest_path_between_intersections(bepis.intersections[0], bepis.intersections[1], 'walk')[bepis.intersections[1]])"""

