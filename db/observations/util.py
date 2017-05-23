


def replace_chars(text):
    #replace some common unicode chars to improve csv readability
    chars = '"“’'
    for char in chars:
        text = text.replace(char,"'")
    return text