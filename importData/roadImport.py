from typing import Dict, List, Tuple

import osmnx as ox
from shapely.coords import CoordinateSequence
from shapely.geometry.linestring import LineString
from shapely.wkt import loads

from heuristic_evaluation.city_model_class import CityModel
from heuristic_evaluation.infrastructure_classes import Intersection, Road
from ownTypes.location import Location


def importKosiceRoads(cityModel: CityModel) -> Tuple[List[Intersection], List[Road]]:
    place_name = "Košice, Slovakia"
    graph = ox.graph_from_place(place_name, network_type="drive")
    nodes, edges = ox.graph_to_gdfs(graph)

    intersections: Dict[int, Intersection] = {}
    roads: List[Road] = []

    for osmid, row in nodes.iterrows():
        intersection: Intersection = Intersection(
            location=Location(x=row["x"], y=row["y"])
        )
        intersections[osmid] = intersection

    maxId: int = max(intersections.keys())

    for index, row in edges.iterrows():  # index: (u,v,key)
        lineString: LineString = row["geometry"]
        if len(lineString.coords) > 2:
            totalPoints: int = len(lineString.coords)
            begin: Intersection = intersections[index[0]]
            for i in range(totalPoints - 2):
                coordinates: CoordinateSequence = lineString.coords[i + 1]
                newPoint = Intersection(
                    location=Location(coordinates[0], coordinates[1])
                )
                maxId += 1
                intersections[maxId] = newPoint

                road = Road(
                    parent_city_model=cityModel,
                    connected_intersections=[begin, newPoint],
                )
                roads.append(road)

                begin = newPoint

            intersectionEnd = intersections[index[1]]
            road = Road(
                parent_city_model=cityModel,
                connected_intersections=[begin, intersectionEnd],
            )
            roads.append(road)
        else:
            intersectionBegin = intersections[index[0]]
            intersectionEnd = intersections[index[1]]
            road = Road(
                parent_city_model=cityModel,
                connected_intersections=[intersectionBegin, intersectionEnd],
            )
            roads.append(road)

    return (list(intersections.values()), roads)
