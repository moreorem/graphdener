from math import sqrt
# PENDING: Add custom binary length in order to cover bigger dimensions


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


if __name__ == '__main__':
    a = iterate_grid(2)
    print([i for i in a])
    print(create_arrowhead([1, 1], [-1, -2]))
