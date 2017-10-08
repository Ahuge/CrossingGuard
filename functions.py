from . import classes
from .exceptions import TypeSyntaxError

OF_CHARS = ["[", "]"]
OR_CHARS = ["|"]


def _validate_buffer(buffer):
    if buffer not in classes.__types__:
        raise NotImplementedError()



def validate_type(typestr):
    entire_buffer = ""
    current_buffer = ""

    root_object = None
    latest_object = None
    while typestr:
        char = typestr.pop(0)
        entire_buffer += char

        if char in OF_CHARS:
            if not latest_object:
                raise TypeSyntaxError(
                    entire_buffer, char + typestr
                )
            break_object = classes.OfClass(char)
            try:
                buffer_object = _validate_buffer(current_buffer)
                current_buffer = ""
            except NotImplementedError:
                raise TypeSyntaxError(
                    entire_buffer, char + typestr
                )
            latest_object.add(
                buffer_object, break_object
            )
        elif char in OR_CHARS:
            if not latest_object:
                raise TypeSyntaxError(
                    entire_buffer, char + typestr
                )
        elif char in
    pass
