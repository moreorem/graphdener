

def _init_node_program(idx):
    program = self.programs[idx]
    program.bind(self.vbo)
    program['u_size'] = 1
    program['u_antialias'] = 1
    program['u_scale'] = self.scale
    return program

def _init_edge_program(idx):
    program = self.programs[idx]
    program.bind(self.vbo)
    program['u_scale'] = self.scale
    return program

def _init_arrow_program(idx):
    program = self.programs[idx]
    program.bind(self.vboar)
    program['size'] = 1.
    program['u_scale'] = self.scale
    return program
