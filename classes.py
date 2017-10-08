from .exceptions import TypeSyntaxError, InvalidChildToken, ValidationError


class OrClass(object):
    pass


class OfClass(object):
    def __init__(self, token):
        super(OfClass, self).__init__()
        if token == "[":
            self.style = 0
        elif token == "]":
            self.style = 1
        else:
            raise TypeSyntaxError("Unknown 'OfClass' %s" % (token))


class BaseToken(object):
    def __init__(self):
        super(BaseToken, self).__init__()
        self.py_type = None
        self.children = []
        self.types = []

    def is_container(self):
        return False

    def add_child(self, type_):
        self.children.append(type_)

    def add_type(self, type_):
        raise NotImplementedError

    def add_of(self, type_):
        raise NotImplementedError

    def valid(self, query):
        for type_ in self.types:
            if isinstance(query, type_):
                return True
        return False

    def add(self, obj, style=None):
        if isinstance(style, OrClass):
            if not self.parent:
                raise NotImplementedError
            if not isinstance(self.parent.children[-1], MultiClass):
                self.parent.add_child = MultiClass(
                    self.parent.children.pop()
                )
            self.parent.children[-1].add_type(obj)
        elif isinstance(style, OfClass):
            if self.is_container():
                self.add_of(obj)
            else:
                raise InvalidChildToken(
                    "Unable to add %s to %s" % (obj.__class__, self.__class__)
                )
        elif style is None:
            self.add_child(obj)
        else:
            raise InvalidChildToken(
                "Unable to add %s to %s" % (obj.__class__, self.__class__)
            )


class CollectionClass(BaseToken):
    def __init__(self, *of_types):
        super(CollectionClass, self).__init__()
        self.of = list(of_types)

    def is_container(self):
        return True

    def add_of(self, type_):
        self.of.append(type_)

    def valid(self, query):
        if super(CollectionClass, self).valid(query):
            for item in query:
                if not any([of.valid(item) for of in self.of]):
                    raise ValidationError(
                        "{item}({itype}) not valid in a {collection} of {types}".format(
                            item=item,
                            itype=type(item),
                            collection=self.py_type,
                            types="[%s]" % (", ".join([t.py_type for t in self.types]))
                        )
                    )


class MultiClass(BaseToken):
    def __init__(self, *types):
        super(MultiClass, self).__init__()
        for obj in types:
            self.children.append(
                obj
            )
            self.types.extend(obj.types)

    def add_type(self, type_):
        self.children.append(
            type_
        )
        self.types.extend(type_.types)


class AnyClass(MultiClass):
    def valid(self, query):
        return True


class ListClass(CollectionClass):
    def __init__(self, *of_types):
        super(ListClass, self).__init__(*of_types)
        self.py_type = "list"
        self.types.extend([ListClass, TupleClass])


class TupleClass(CollectionClass):
    def __init__(self, *of_types):
        super(TupleClass, self).__init__(*of_types)
        self.py_type = "tuple"
        self.types.extend([TupleClass, ListClass])


class IntClass(BaseToken):
    def __init__(self):
        super(IntClass, self).__init__()
        self.py_type = "int"
        self.types.extend([IntClass, FloatClass])


class FloatClass(BaseToken):
    def __init__(self):
        super(FloatClass, self).__init__()
        self.py_type = "float"
        self.types.extend([FloatClass, IntClass])


class StrClass(BaseToken):
    def __init__(self):
        super(StrClass, self).__init__()
        self.py_type = "str"
        self.types.extend([StrClass])


__types__ = {
    "Any": {
        "description": "Any Python object",
        "object": AnyClass,
    },
    "List": {
        "description": "List object in python",
        "object": ListClass,
    },
    "int": {
        "description": "Integer object",
        "object": IntClass
    },
    "str": {
        "description": "String object",
        "object": StrClass
    }

}