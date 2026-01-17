class ImmutableMetaclass(type):
    def __setattr__(self, key, value):
        raise AttributeError(f"Cannot assign attribute of immutable class {self}")


class Immutable(metaclass=ImmutableMetaclass):
    def __setattr__(self, key, value):
        raise AttributeError(f"Cannot assign attribute of immutable class {type(self)}")
