from flask import Blueprint
from itertools import count

filters = Blueprint('filters', __name__, )


@filters.app_template_filter('date')
def filter_datetime(date_value='', format='%B %d, %Y'):
    return date_value.strftime(format)


@filters.app_template_filter('stars')
def filter_stars(rating=''):

    stars = [
        '<i class="material-icons">thumb_down</i>',
        '<i class="material-icons">star_half</i>',
        '<i class="material-icons">star</i>',
        '<i class="material-icons">star</i><i class="material-icons">star_half</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star_half</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star_half</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star_half</i>',
        '<i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i><i class="material-icons">star</i>'
    ]
    index = int(rating)
    return stars[index]

@filters.app_template_filter('note')
def filter_notes_label(notes=''):
    number = len(notes)
    if number == 1:
        return format('%s Tasting Note' % str(number))
    elif number > 1:
        return format('%s Tasting Notes' % str(number))
    else:
        return None
