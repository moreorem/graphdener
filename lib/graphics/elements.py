from os import path as op

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


