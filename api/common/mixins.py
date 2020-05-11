class ReprMixin():

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        cls_name = self.__class__.__name__
        for attr in ["slug", "name", "username", "id"]:
            if value := getattr(self, attr, None):
                return f"<{cls_name} {attr}={value}>"
        return f"<{cls_name}>"
