# encoding: utf-8
# Required modules:
# inspect

import inspect

"""Use alias (validate) to validate a variable. If you prefer to raise 
an exception or include context in custom error message, tick the 
corresponding params in valContext method. 
This module has two handy methods: validateType and validateAttr."""


def valContext(input_data, validationFunction, *args, message="", eject=True, popContextMessage=True):
    """Use alias (validate) to validate a variable. If you prefer to raise 
    an exception or include context in custom error message, tick the 
    corresponding params in valContext method. """
    if not isinstance(message, str):
        SpecialTypeError = TypeError("Enter a valid error message in string.")
        raise SpecialTypeError
    if not validationFunction(input_data, *args):
        defaultMessage = f"Expect {validationFunction}({input_data}, {args}) to be True, but got {validationFunction(input_data, *args)}"
        if popContextMessage:
            # Is a feature that should be used only in debugging process.
            contextFrameInfo = inspect.getouterframes(
                inspect.currentframe())[1]
            # A frameinfo object that can be subscripted: frame, file, lineno, method_name, code_context, index
            __file = contextFrameInfo[1]
            __lineno = contextFrameInfo[2]
            __method_name = contextFrameInfo[3]
            __code_context = contextFrameInfo[4]

            full_context_message = f'Below is the context info:\nIn {__file}, at line {__lineno}:\n{"="*7}\n{__code_context}\n{"="*7}'
            defaultMessage = f"{message[0].lower()}{message[1:]}"
            message += f"In method {__method_name}, {defaultMessage} {full_context_message}"
            print(message)
        else:
            if message == "":
                message = defaultMessage
        if eject:
            raise TypeError(message)
        return TypeError(message)
    return False


def validate(input_data, validationFunction, *args, message, eject=True):
    valContext(input_data, validationFunction, *args, message=message,
               eject=eject, popContextMessage=False)


def valType(input_data, instanceOf, message, eject=True):
    valContext(input_data, isinstance, instanceOf, message=message,
               eject=eject, popContextMessage=False)


def valAttr(input_data, hasAttr, message, eject=True):
    valContext(input_data, hasattr, hasAttr, message=message,
               eject=eject, popContextMessage=False)
