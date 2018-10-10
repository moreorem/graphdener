import numpy as np
import math
from ..statics import ARROWHEAD_SIZE

def create_arrowhead(A, B, marker_size):
    """
    Use trigonometry to calculate the arrowheads vertex positions according to the edge direction.

    Parameters
    ----------
    A : array
        x,y Starting point of edge
    B : array
        x,y Ending point of edge

    Returns
    -------
    B, v1, v2 : tuple
        The point of head, the v1 xy and v2 xy points of the two base vertices of the arrowhead.
    """
    w = ARROWHEAD_SIZE  # Half of the triangle base width
    h = w / 0.26794919243  # tan(15)

    AB = [B[0] - A[0], B[1] - A[1]]
    mag = math.sqrt(AB[0]**2.0 + AB[1]**2.0)
    if mag == 0:
        mag = 1.0
    d = (marker_size - 5) / 1000.0 #0.045  # Distance from node

    u0 = AB[0] / mag
    u1 = AB[1] / mag
    U = [u0, u1]  # Unit vector of AB

    V = [-U[1], U[0]]  # Unit vector perpendicular to AB

    C = [B[0] - d * u0, B[1] - d * u1]

    v1 = [C[0] - h * U[0] + w * V[0], C[1] - h * U[1] + w * V[1]]
    v2 = [C[0] - h * U[0] - w * V[0], C[1] - h * U[1] - w * V[1]]

    return (C, v1, v2)


def get_segments_pos(vPos, edgeList):
    return [[vPos[i[0]], vPos[i[1]]] for i in edgeList]


def set_marker_data(pos, size, color, pixelScale):
    n = len(pos)
    # Initialize node data
    data = np.zeros(n, dtype=[('a_position', np.float32, 3),
                              ('a_fg_color', np.float32, 4),
                              ('a_bg_color', np.float32, 4),
                              ('a_size', np.float32, 1),
                              ('a_linewidth', np.float32, 1),
                              ])

    data['a_position'] = pos
    data['a_fg_color'] = 0, 0, 0, 1

    if color is None:
        color = np.random.uniform(0.5, 1., (n, 3))
    else:
        color = np.array(list(color))
        data['a_bg_color'] = np.hstack((color, np.ones((n, 1))))
        # Size of the markers
        data['a_size'] = np.array(np.ones(n) * (size * pixelScale))
        data['a_linewidth'] = 1. * pixelScale

    return data
