from os import path as op
import numpy as np
from .util import create_arrowhead, get_segments_pos

this_dir = op.abspath(op.dirname(__file__))
GLFOLDER = '/glsl/'
FULLPATH = this_dir + GLFOLDER


class GlslBridge():
    def __init__(self):
        # TODO: Create separate objects for each collection (node, edge, arrow)
        with open(op.join(FULLPATH, 'n_vert.glsl'), 'rb') as f1:
            n_vert = f1.read().decode('ASCII')
        with open(op.join(FULLPATH, 'n_frag.glsl'), 'rb') as f2:
            n_frag = f2.read().decode('ASCII')
        with open(op.join(FULLPATH, 'e_vert.glsl'), 'rb') as f3:
            e_vert = f3.read().decode('ASCII')
        with open(op.join(FULLPATH, 'e_frag.glsl'), 'rb') as f4:
            e_frag = f4.read().decode('ASCII')
        with open(op.join(FULLPATH, 'a_vert.glsl'), 'rb') as f5:
            a_vert = f5.read().decode('ASCII')
        with open(op.join(FULLPATH, 'a_frag.glsl'), 'rb') as f6:
            a_frag = f6.read().decode('ASCII')

        self.vertgl = [n_vert, n_frag]
        self.edgegl = [e_vert, e_frag]
        self.argl = [a_vert, a_frag]


class ArrowHead():
    '''
    n: int
    represents number of edges
    '''

    def __init__(self, nodePos, edges, marker_size):
        # number of total points to draw n arrows is 3 * n
        # na = 3 * n
        BCD = []
        self.marker_size = marker_size
        vPos = nodePos[:, 0:2].tolist()
        linesAB = get_segments_pos(vPos, edges)

        for line in linesAB:
            B, C, D = create_arrowhead(line[0], line[1], self.marker_size)
            BCD.append(B)
            BCD.append(C)
            BCD.append(D)

        na = len(BCD)
        # Set vertex number for total of arrowheads
        self.arrowData = np.zeros(na, dtype=[
            ('a_position', np.float32, 2),
            ('a_fg_color', np.float32, 4),
            ('a_bg_color', np.float32, 3),
        ])
        # Divide arrowhead vertex number by 3 to create color for every three vertices
        col_n = na // 3
        c = np.random.uniform(0.5, 1., (col_n, 3))
        self.arrowData['a_bg_color'] = np.repeat(c, [3], axis=0)

    def setArrowPos(self, nodePos, edgesIndex):
        vPos = nodePos[:, 0:2].tolist()
        linesAB = get_segments_pos(vPos, edgesIndex)
        aPos = np.array(self.__calcArrow(linesAB))
        self.arrowData['a_position'] = aPos

    def __calcArrow(self, segment):
        BCD = []
        for line in segment:
            B, C, D = create_arrowhead(line[0], line[1], self.marker_size)
            BCD.append(B)
            BCD.append(C)
            BCD.append(D)
        return BCD

    def getArrowData(self):
        return self.arrowData
