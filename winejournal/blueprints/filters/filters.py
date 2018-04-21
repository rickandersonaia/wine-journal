from flask import Blueprint

filters = Blueprint('filters', __name__, )


@filters.app_template_filter('date')
def filter_datetime(date_value = '', format='%B %d, %Y'):
    return date_value.strftime(format)
