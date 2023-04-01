from typing import Dict, List, Tuple

import osmnx as ox
from geopandas import GeoDataFrame
from shapely.coords import CoordinateSequence
from shapely.geometry.linestring import LineString

from heuristic_evaluation.city_model_class import CityModel
from heuristic_evaluation.infrastructure_classes import Intersection, Road
from ownTypes.location import Location


def addRoadToRoads(
    begin: Intersection, end: Intersection, roads: List[Road], cityModel: CityModel
) -> None:
    road = Road(parent_city_model=cityModel, connected_intersections=[begin, end])
    roads.append(road)


def getNodesAndEdgesFromCity(
    placeName: str = "Košice, Slovakia",
) -> Tuple[GeoDataFrame, GeoDataFrame]:
    graph = ox.graph_from_place(placeName, network_type="drive")
    return ox.graph_to_gdfs(graph)


def importKosiceRoads(
    nodes: GeoDataFrame, edges: GeoDataFrame, cityModel: CityModel
) -> Tuple[List[Intersection], List[Road]]:
    intersections: Dict[int, Intersection] = {}
    roads: List[Road] = []

    for osmid, row in nodes.iterrows():
        intersection: Intersection = Intersection(
            location=Location(lon=row["x"], lat=row["y"])
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

                addRoadToRoads(begin, newPoint, roads, cityModel)

                begin = newPoint

            intersectionEnd = intersections[index[1]]
            addRoadToRoads(begin, intersectionEnd, roads, cityModel)
        else:
            intersectionBegin = intersections[index[0]]
            intersectionEnd = intersections[index[1]]
            addRoadToRoads(intersectionBegin, intersectionEnd, roads, cityModel)

    return (list(intersections.values()), roads)
