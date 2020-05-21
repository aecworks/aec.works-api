from django.db.models.fields import Field
from django.db.models.lookups import Transform


class Floor(Transform):
    """
    Floor is included in 3 -
    required to annotate mptt descendent count for comments
    """

    function = "FLOOR"
    lookup_name = "floor"


Field.register_lookup(Floor)
