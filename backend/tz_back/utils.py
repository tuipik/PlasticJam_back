class RepresentableMixin:

    def __str__(self):
        return f'<{self.__class__.__name__}>'
