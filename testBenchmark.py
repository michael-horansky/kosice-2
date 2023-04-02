from time import time
from typing import List

from heuristic_evaluation.city_model_class import CityModel
from heuristic_evaluation.infrastructure_classes import Building
from importData.buildingImport import importBuildings
from importData.roadImport import getNodesAndEdgesFromCity, importKosiceRoads
from ownTypes.location import Location

print("Initialising city model...")

cityModel: CityModel = CityModel()

max_lat = 48.72780584173411
max_lon = 21.2623857571228
min_lat = 48.71589420381176
min_lon = 21.25281311948872

def is_in_rect(loc):
    lon, lat = loc.pair
    if lon > min_lon and lon < max_lon and lat > min_lat and lat < max_lat:
        return(True)
    else:
        return(False)

print("Loading buildings...")

buildings: List[Building] = importBuildings(inputFile="POI.csv")
for building in buildings:
    if is_in_rect(building.location):
        cityModel.add_building(building)

print("Loading infrastructure...")

nodes, edges = getNodesAndEdgesFromCity()
intersections, roads = importKosiceRoads(nodes=nodes, edges=edges, cityModel=cityModel)

print("Creating representation of datasets...")

for intersection in intersections:
    if is_in_rect(intersection.location):
        cityModel.add_intersection(intersection)

for road in roads:
    if is_in_rect(road.connected_intersections[0].location) and is_in_rect(road.connected_intersections[1].location):
        cityModel.add_road(road.connected_intersections)

loc1 = Location(lat=48.722046755953116, lon=21.255898406677275)
print(f"Location selected at lat = {loc1.lat}, lon = {loc1.lon}")

#loc2 = Location(lat=48.7497041, lon=21.2825586)

print("Evaluating score based on the weighted time distance from facilities...")
start = time()

loc1_score = cityModel.find_score_of_location(
        start_location=loc1, mode_of_transportation="walk"
    )
end = time() - start

print("  -------------------------------")
print(f"  Final evaluation: weighted proximity of this location is {loc1_score / 60:.2f} min")
print( "  (This is roughly how long a walk to an unspecified available facility should take from here)")

print(f"Scoring algorithm runtime: {end:.2f}s")
