from .statics import COLUMN_TYPES
# Counter counts the number of occurrences of each item
from collections import Counter


def iterate_grid(d):
    """
    Returns a generator over a square grid of d dimensions

    Keyword arguments:
    d -- the m == n dimension of the grid e.g. 2x2
    @type d: int
    """
    binlen = '{{0:0{}b}}'.format(d)

    for i in range(d**2):
        y = [int(x) for x in list(binlen.format(i))]
        yield y


def regex_builder():
    pass


def alter_conc(list1, list2):
    """
    Concatenates two lists into a new one alternatively. List2 must be 1 element shorter than list1.

    Parameters
    ----------
    list1 : list of length n
    list2 : list of length n - 1

    Returns
    -------
    altList : list
        list of length 2n - 1
    """

    result = [None] * (len(list1) + len(list2))
    try:
        result[::2] = list1
        result[1::2] = list2
        return result
    except ValueError as e:
        print("list2 must be -1 shorter than list1", e)

# FIXME: Ideal regex is this: (?P<n_id>\d+)\s+"(?P<n_label>[^"]*)"(?:\s+"(?P<n_type>[^"]*)")?
def type_to_regex(t):
    options = {'str': '*' + ')', 'qstr': '[^"]*' + ')?', 'int': r'\d+' + ')', '': ''}
    try:
        return options[t]
    except KeyError as e:
        print("Invalid type", e)


def has_quotes(t):
    if t in ['qstr']:
        # Remove ? if there is problem
        return r'"?'
    else:
        return ''


def get_pattern(columns, delims):
    """
    Create regular expression pattern according to user input
    """
    print("getting pattern")
    # Rename columns that have the same names to prevent regex error
    rename_duplicates(columns)
    # FIXME: Too many brackets when removing columns
    cols = ['{}{}{}{}'.format(
        has_quotes(COLUMN_TYPES[clean(name)]),
        parse_empty(name),
        type_to_regex(COLUMN_TYPES[clean(name)]),
        has_quotes(COLUMN_TYPES[clean(name)])
    ) for name in columns]
    # Create the node regular expression string
    return ''.join(alter_conc(delims, cols))


def parse_empty(name):
        if name == '-':
            return ''
        else:
            return '(?P<' + name + '>'


# Returns a dictionary of column names and types to be mapped in the backend for recognizing regex captures
def get_col_info(columnNames):
    result = {}
    for name in columnNames:
        name = clean(name)
        if name not in ['-', '']:
            result[name] = COLUMN_TYPES[name]
    return result


def rename_duplicates(mylist):
    # so we have: {'name':3, 'state':1, 'city':1, 'zip':2}
    counts = Counter(mylist)
    for s, num in counts.items():
        # ignore strings that only appear once
        if num > 1 and len(s) > 1:
            # suffix starts at 1 and increases by 1 each time
            for suffix in range(1, num + 1):
                # replace each appearance
                mylist[mylist.index(s)] = s + str(suffix)


def clean(name):
    if len(name) > 1:
        try:
            if type(eval(name[-1])) == int:
                return name[:-1]
        except:
            return name
    else:
        return name
