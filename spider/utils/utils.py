def string_strip(text):
    """
    Wipe out \xa0, \r, \n space etc.. in text
    :param text: sample: "\n          397.0\xa0\xa0"
    :return: 397.0
    """
    if text is None:
        return ""
    else:
        return "".join(text.split())
