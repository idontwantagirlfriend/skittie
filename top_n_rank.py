# encoding: utf-8
# Required modules:
# inspect (in input validation)

import inspect


def top_n_rank(element_list, top_num, step_word: set = {"的", "有", "和", "了", "与", "为", "在", "上", "等", "而", "以", "如", "之", "只",
                                                                   "是", "都", "即", "后", "中", "同", "从", "及", "也", "对", "到"}):
    """Applies to any (duplicate) element list. Calculate the top_num most frequent element(s).
    If a negative value is used for top_num, calculate the top_num rarest element(s).
    Return a list.
    This method is initially for calculating word frequency for Chinese text samples."""
    valAttr(element_list, "__iter__", message=f"The argument {element_list} doesn\'t look right. The element_list argument should be an iterable. You might consider using list({element_list}).")
    valType(top_num, int, message=f"The argument {top_num} doesn\'t look right. The top_num argument should be an integer.")
    valAttr(step_word, "__iter__", message=f"The argument {step_word} doesn\'t look right. The step_word argument should be an iterable.")
    frequency = {}
    for i in element_list:
        frequency[i] = frequency.get(i, 0)+1

    filtered_frequency = []  # is a list
    for i in frequency:
        if not i in step_word:
            filtered_frequency.append([i, frequency[i]])
    filtered_frequency = sorted(
        filtered_frequency, key=lambda x: x[1], reverse=True)

    if (-len(filtered_frequency)-1) < top_num < (len(filtered_frequency)+1):
        if top_num > -1:
            # Top top_num frequent element(s).
            rank = filtered_frequency[:top_num]
        else:
            # Top top_num rare element(s) if top_num is negative.
            rank = filtered_frequency[top_num:]
    else:
        rank = filtered_frequency
        if __name__ == "__main__":
            message = f"Given rank number exceeds max rank ({len(filtered_frequency)})."
            print(message)

    return rank


# From the validate module. Confer my kit. 
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

