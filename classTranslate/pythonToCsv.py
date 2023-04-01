import csv
from typing import List

from heuristic_evaluation.infrastructure_classes import Intersection, Road

INTERSECTIONS_PATH = "intersections.csv"
ROADS_PATH = "roads.csv"


def intersectionToCsvRow(intersection: Intersection) -> list:
    return [intersection.id, intersection.location.lon, intersection.location.lat]


def intersectionsToCsv(intersections: List[Intersection]) -> None:
    id = 1
    with open("intersections.csv", "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Id", "Lon", "Lat"])
        for intersection in intersections:
            intersection.setId(id)
            id += 1
            writer.writerow(intersectionToCsvRow(intersection=intersection))


def roadToCsvRow(road: Road) -> list:
    return [road.connected_intersections[0].id, road.connected_intersections[1].id]


def roadsToCsv(roads: List[Road]) -> None:
    with open("roads.csv", "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Begin", "End"])
        for road in roads:
            writer.writerow(roadToCsvRow(road=road))


def translateAll(roads: List[Road], intersections: List[Intersection]) -> None:
    intersectionsToCsv(intersections=intersections)
    roadsToCsv(roads=roads)
