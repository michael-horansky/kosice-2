from heuristic_evaluation.city_model_class import *


kosice = CityModel()
kosice.add_intersection(Location(21.238454903302088, 48.69470206219284)) # OC optima
kosice.add_intersection(Location(21.263561595515494, 48.69767209785608)) #kongres hotel
kosice.add_road([kosice.intersections[0], kosice.intersections[1]])

print(kosice.roads[0])
print(kosice.roads[0].get_physical_length())