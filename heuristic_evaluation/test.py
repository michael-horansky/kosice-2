from city_model_class import *


kosice = CityModel()
kosice.add_intersection(Location(21.2385988, 48.6946569)) # OC optima
kosice.add_intersection(Location(21.2632647, 48.6975202)) #kongres hotel
kosice.add_road(kosice.intersections[0], kosice.intersections[1])

print(kosice.roads[0])
