

class TypeSyntaxError(BaseException):
    def __init__(self, previous_str, next_str):
        error_msg = "Invalid Syntax here:"
        line1 = previous_str + next_str
        spacer_length = (len(previous_str) + len(self.__class__.__name__) + 2)
        if spacer_length >= len(error_msg):
            line2 = error_msg + (" " * (spacer_length - len(error_msg)))
            line2 += "^"
        else:
            line2 = " " * spacer_length
            line2 += "^"
            line2 += "\n" + error_msg
        super(TypeSyntaxError, self).__init__(
            "\n".join([line1, line2])
        )


class InvalidChildToken(BaseException):
    pass


class ValidationError(BaseException):
    pass
