from flask import Blueprint, current_app
from flask_caching import Cache

main = Blueprint('main', __name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})

from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)