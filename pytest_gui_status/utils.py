def s(input_):
    ''' Convert str or uncode or bytes to str.
    If list, do it for all of them.
    If others, return as is. '''

    import sys
    PY3 = sys.version_info > (3,)

    if isinstance(input_, list):
        return [s(ele) for ele in input_]

    try:
        if PY3:
            assert(type(input_) in [str, bytes])
        else:
            assert(type(input_) in [str, unicode, bytes])
    except AssertionError:
        return input_

    if PY3:
        if type(input_) == bytes:
            str_ = bytes.decode(input_)
            return str_

    # either str or unicode
    str_ = str(input_)
    return str_
