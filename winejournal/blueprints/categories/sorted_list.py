from winejournal.extensions import db
from winejournal.data_models.categories import Category


def get_unsorted_categories():
    return db.session.query(Category).all()


def get_sorted_categories():
    top_list = {}
    cats = get_unsorted_categories()
    for cat_1 in cats:
        if cat_1.parent_id == 0:
            top_list[cat_1.id] = cat_1.name
            for cat_2 in cats:
                if cat_2.parent_id == cat_1.id:
                    top_list[cat_2.id] = '- ' + cat_2.name
                    for cat_3 in cats:
                        if cat_3.parent_id == cat_2.id:
                            top_list[cat_3.id] = '-- ' + cat_3.name

    return top_list
