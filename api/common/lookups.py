from django.db.models.fields import Field
from django.db.models.lookups import Transform


class Floor(Transform):
    function = "FLOOR"
    lookup_name = "floor"


Field.register_lookup(Floor)
