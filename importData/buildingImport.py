import pandas as pd

from heuristic_evaluation.infrastructure_classes import Building


def importBuildings(inputFile: str) -> list[Building]:
    result: list[Building] = []
    buildings: pd.DataFrame = pd.read_csv(filepath_or_buffer=inputFile)

    for _, row in buildings.iterrows():
        building: Building = Building(
            location=(row["x"], row["y"]),
            service=row["typ_0"],
            surface_area=None,
            parameters=None,
        )

        result.append(building)

    return result
