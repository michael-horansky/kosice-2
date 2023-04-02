from time import time
from typing import List

from heuristic_evaluation.city_model_class import CityModel
from heuristic_evaluation.infrastructure_classes import Building
from importData.buildingImport import importBuildings
from importData.roadImport import getNodesAndEdgesFromCity, importKosiceRoads
from ownTypes.location import Location

cityModel: CityModel = CityModel()

print("vytvoril som city model")

buildings: List[Building] = importBuildings(inputFile="POI.csv")
for building in buildings:
    cityModel.add_building(building)

print("mame buildings")

nodes, edges = getNodesAndEdgesFromCity()
intersections, roads = importKosiceRoads(nodes=nodes, edges=edges, cityModel=cityModel)

print("mame intersections")

for intersection in intersections:
    cityModel.add_intersection(intersection)

for road in roads:
    cityModel.add_road(road.connected_intersections)

print("vytvoril som mesto")

loc1 = Location(lat=48.7385041, lon=21.2814586)
loc2 = Location(lat=48.7497041, lon=21.2825586)

print("idem na to drz mi palce")
start = time()
print(
    cityModel.find_score_of_location(
        start_location=loc1, mode_of_transportation="walk"
    )
)
end = time() - start

print(f"Trvalo to {end} ty gec")
