from models import *

for model in [
    Asset, Attr_type, Bounds, Path, Attribute, Format, Geom_type, Drive]:
    if not hasattr(model, '__unicode__'):  # and hasattr(model, 'name'):
        model.__unicode__ = lambda self, model=model: getattr(self, 'name', model.__name__)
