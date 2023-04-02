import networkx as nx

from heuristic_evaluation.infrastructure_classes import Intersection, Road


class Distance:

    g: nx.Graph

    def __init__(self):
        self.g = nx.Graph()

    def addIntersection(self, intersection: Intersection) -> None:
        if intersection.id is None:
            raise ValueError("ID must be set")
        self.g.add_node(intersection.id)

    def addRoad(self, road: Road) -> None:
        self.g.add_edge(
            road.connected_intersections[0].id,
            road.connected_intersections[1].id,
            weight=road.connected_intersections[0].location.distance(
                road.connected_intersections[1].location
            ),
        )

    def shortestDistanceBetweenTwoIntersections(
        self, intersectionOne: Intersection, intersectionTwo: Intersection
    ) -> float:
        #print(nx.dijkstra_path(self.g, intersectionOne.id, intersectionTwo.id))
        return nx.dijkstra_path_length(self.g, intersectionOne.id, intersectionTwo.id)

