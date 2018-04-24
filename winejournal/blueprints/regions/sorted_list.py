from winejournal.data_models.regions import Region
from winejournal.extensions import db


def get_unsorted_regions():
    return db.session.query(Region).all()


def get_sorted_regions():
    sorted_region_list = {}
    regions = get_unsorted_regions()

    for region_1 in regions:
        if region_1.parent_id == 0:
            sorted_region_list[region_1.id] = region_1.name
            for region_2 in regions:
                if region_2.parent_id == region_1.id:
                    sorted_region_list[region_2.id] = '- ' + region_2.name
                    for region_3 in regions:
                        if region_3.parent_id == region_2.id:
                            sorted_region_list[
                                region_3.id] = '-- ' + region_3.name
    return sorted_region_list
