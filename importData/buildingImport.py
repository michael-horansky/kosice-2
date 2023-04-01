from typing import List

import pandas as pd

from heuristic_evaluation.infrastructure_classes import Building
from ownTypes.location import Location

def encode_service(human_readable_type):
    if 'ambulancia pre deti' in human_readable_type:
        return('children_clinic')
    if 'Pošty' in human_readable_type:
        return('post_office')
    if 'zub' in human_readable_type:
        return('dental_clinic')
    if 'restaurant' in human_readable_type or 'reštaurácia' in human_readable_type:
        return('restaurant')
    if 'playground' in human_readable_type or 'ihrisko' in human_readable_type:
        return('playground')
    if 'supermarket' in human_readable_type:
        return('supermarket')
    if 'ZS' in human_readable_type:
        return('elementary_school')
    if 'psy' in human_readable_type:
        return('dog_enclosure')
    if 'chemist' in human_readable_type or 'drog' in human_readable_type:
        return('drug_store')
    if 'parcel' in human_readable_type or 'doručovacie' in human_readable_type:
        return('parcel_locker')
    if 'MHD' in human_readable_type:
        return('bus_stop')
    if 'MS' in human_readable_type:
        return('kindergarten')
    if 'fitness' in human_readable_type:
        return('fitness')
    if 'bar' in human_readable_type:
        return('bar')
    if 'pub' in human_readable_type:
        return('pub')
    if 'fast' in human_readable_type:
        return('fast_food')
    if 'pharmacy' in human_readable_type or 'káreň' in human_readable_type:
        return('pharmacy')
    if 'convenience' in human_readable_type or 'potraviny' in human_readable_type:
        return('convenience')
    if 'cafe' in human_readable_type:
        return('cafe')
    if 'ambulancia pre dospe' in human_readable_type:
        return('general_clinic')
    return('UNCATEGORIZED')
    
    


def importBuildings(inputFile: str) -> List[Building]:
    result: List[Building] = []
    buildings: pd.DataFrame = pd.read_csv(filepath_or_buffer=inputFile)

    for _, row in buildings.iterrows():
        building: Building = Building(
            location=Location(lon=row["x"], lat=row["y"]),
            service=encode_service(row["typ_0"]),
            surface_area=None,
            parameters=None,
        )

        result.append(building)

    return result
