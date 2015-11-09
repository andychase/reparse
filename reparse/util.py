import regex

def separate_string(string):
    """
    >>> separate_string("test <2>")
    (['test ', ''], ['2'])
    """
    string_list = regex.split(r'<(?![!=])', regex.sub(r'>', '<', string))
    return string_list[::2], string_list[1::2]  # Returns even and odd elements


def overlapping(start1, end1, start2, end2):
    """
    >>> overlapping(0, 5, 6, 7)
    False
    >>> overlapping(1, 2, 0, 4)
    True
    >>> overlapping(5,6,0,5)
    False
    """
    return not ((start1 <= start2 and start1 <= end2 and end1 <= end2 and end1 <= start2) or
                (start1 >= start2 and start1 >= end2 and end1 >= end2 and end1 >= start2))


def overlapping_at(start, end, current):
    for current_index, (_, c_start, c_end) in enumerate(current):
        if overlapping(c_start, c_end, start, end):
            yield current_index


def remove_lower_overlapping(current, higher):
    """
    >>> remove_lower_overlapping([], [('a', 0, 5)])
    [('a', 0, 5)]
    >>> remove_lower_overlapping([('z', 0, 4)], [('a', 0, 5)])
    [('a', 0, 5)]
    >>> remove_lower_overlapping([('z', 5, 6)], [('a', 0, 5)])
    [('z', 5, 6), ('a', 0, 5)]
    """
    for (match, h_start, h_end) in higher:
        overlaps = list(overlapping_at(h_start, h_end, current))
        for overlap in overlaps:
            del current[overlap]
        if len(overlaps) > 0:
            # Keeps order in place
            current.insert(overlaps[0], (match, h_start, h_end))
        else:
            current.append((match, h_start, h_end))

    return current
