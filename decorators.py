from . import classes


def types(**definition_kwargs):
    def function_wrapper(func):
        func_args = func.func_code.co_varnames
        func_defaults = func.func_defaults
        
        def function_caller(**kwargs):
             for key in kwargs:
                 if key in 
