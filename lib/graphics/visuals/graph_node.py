from vispy.visuals.shaders import Function, Variable
from vispy.visuals.visual import Visual
from vispy.gloo import VertexBuffer, _check_valid
import numpy as np


vert = """
#version 120

// Uniforms
// ------------------------------------
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_linewidth;
uniform float u_antialias;
uniform float u_size;

// Attributes
// ------------------------------------
attribute vec3  a_position;
attribute vec4  a_fg_color;
attribute vec4  a_bg_color;
attribute float a_linewidth;
attribute float a_size;

// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

void main (void) {
    v_linewidth = a_linewidth;
    v_antialias = u_antialias;
    v_fg_color  = a_fg_color;
    v_bg_color  = a_bg_color;
    gl_Position = $transform(vec4(a_position,1.0));

    gl_PointSize = ($v_size) + 2*(v_linewidth + 1.5*v_antialias);
}
"""

frag = """
#version 120

// Constants
// ------------------------------------
#define resolution vec2(500.0, 500.0)
#define Thickness 0.003
// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

// Functions
// ------------------------------------
float marker(vec2 P, float size)
{
    float r = length((P.xy - vec2(0.5,0.5))*size);
    r -= v_size/2;
    return r;
}

// Main
// ------------------------------------
void main()
{
    // size turns outline to circle
    float size = v_size +2*(v_linewidth + 1.5*v_antialias);
    float t = v_linewidth/2.0-v_antialias;

    if ($v_size <= 0.)
        discard;

    float edgealphafactor = min(v_edgewidth, 1.0);

    float size = $v_size + 4.*(edgewidth + 1.5*v_antialias);

    // The marker function needs to be linked with this shader
    float r = marker(gl_PointCoord, size);

    float d = abs(r) - t;
    if( r > (v_linewidth/2.0+v_antialias))
    {
        discard;
    }
    else if( d < 0.0 )
    {
       gl_FragColor = v_fg_color;
    }
    else
    {
        float alpha = d/v_antialias;
        alpha = exp(-alpha*alpha);
        if (r > 0)
            gl_FragColor = vec4(v_fg_color.rgb, alpha*v_fg_color.a);
        else
            gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
    }
}
"""


class GNodeVisual(Visual):
    """ Visual displaying node symbols.
    """
    def __init__(self, **kwargs):
        self._vbo = VertexBuffer()
        self._v_size_var = Variable('varying float v_size')
        self._symbol = None
        self._marker_fun = None
        self._data = None
        self.antialias = 1
        self.scaling = False
        Visual.__init__(self, vcode=vert, fcode=frag)
        self.shared_program.vert['v_size'] = self._v_size_var
        self.shared_program.frag['v_size'] = self._v_size_var
        self.set_gl_state(depth_test=True, blend=True,
                          blend_func=('src_alpha', 'one_minus_src_alpha'))
        self._draw_mode = 'points'
        if len(kwargs) > 0:
            self.set_data(**kwargs)
        self.freeze()

    def set_data(self, pos=None, symbol='o', size=10., edge_width=1.,
                 edge_width_rel=None, edge_color='black', face_color='white',
                 scaling=False):
        """ Set the data used to display this visual.

        Parameters
        ----------
        pos : array
            The array of locations to display each symbol.
        symbol : str
            The style of symbol to draw (see Notes).
        size : float or array
            The symbol size in px.
        edge_width : float | None
            The width of the symbol outline in pixels.
        edge_width_rel : float | None
            The width as a fraction of marker size. Exactly one of
            `edge_width` and `edge_width_rel` must be supplied.
        edge_color : Color | ColorArray
            The color used to draw each symbol outline.
        face_color : Color | ColorArray
            The color used to draw each symbol interior.
        scaling : bool
            If set to True, marker scales when rezooming.

        Notes
        -----
        Allowed style strings are: disc, arrow, ring, clobber, square, diamond,
        vbar, hbar, cross, tailed_arrow, x, triangle_up, triangle_down,
        and star.
        """
        assert (isinstance(pos, np.ndarray) and
                pos.ndim == 2 and pos.shape[1] in (2, 3))
        if (edge_width is not None) + (edge_width_rel is not None) != 1:
            raise ValueError('exactly one of edge_width and edge_width_rel '
                             'must be non-None')
        if edge_width is not None:
            if edge_width < 0:
                raise ValueError('edge_width cannot be negative')
        else:
            if edge_width_rel < 0:
                raise ValueError('edge_width_rel cannot be negative')
        self.symbol = symbol
        self.scaling = scaling

        edge_color = ColorArray(edge_color).rgba
        if len(edge_color) == 1:
            edge_color = edge_color[0]

        face_color = ColorArray(face_color).rgba
        if len(face_color) == 1:
            face_color = face_color[0]

        n = len(pos)
        data = np.zeros(n, dtype=[('a_position', np.float32, 3),
                                  ('a_fg_color', np.float32, 4),
                                  ('a_bg_color', np.float32, 4),
                                  ('a_size', np.float32, 1),
                                  ('a_edgewidth', np.float32, 1)])
        data['a_fg_color'] = edge_color
        data['a_bg_color'] = face_color
        if edge_width is not None:
            data['a_edgewidth'] = edge_width
        else:
            data['a_edgewidth'] = size*edge_width_rel
        data['a_position'][:, :pos.shape[1]] = pos
        data['a_size'] = size
        self.shared_program['u_antialias'] = self.antialias  # XXX make prop
        self._data = data
        if self._symbol is not None:
            # If we have no symbol set, we skip drawing (_prepare_draw
            # returns False). This causes the GLIR queue to not flush,
            # and thus the GLIR queue fills with VBO DATA commands, resulting
            # in a "memory leak". Thus only set the VertexBuffer data if we
            # are actually going to draw.
            self._vbo.set_data(data)
            self.shared_program.bind(self._vbo)
        self.update()

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        if symbol == self._symbol:
            return
        if (symbol is not None and self._symbol is None and
                self._data is not None):
            # Allow user to configure symbol after a set_data call with
            # symbol=None. This can break down if the user does a consecutive
            # marker.symbol = 'disc'
            # marker.symbol = None
            # without drawing. At this point the memory leaking ensues
            # but this case is unlikely/makes no sense.
            self._vbo.set_data(self._data)
            self.shared_program.bind(self._vbo)
        self._symbol = symbol
        if symbol is None:
            self._marker_fun = None
        else:
            _check_valid('symbol', symbol, marker_types)
            self._marker_fun = Function(_marker_dict[symbol])
            self._marker_fun['v_size'] = self._v_size_var
            self.shared_program.frag['marker'] = self._marker_fun
        self.update()

    def _prepare_transforms(self, view):
        xform = view.transforms.get_transform()
        view.view_program.vert['transform'] = xform

    def _prepare_draw(self, view):
        if self._symbol is None:
            return False
        view.view_program['u_px_scale'] = view.transforms.pixel_scale
        if self.scaling:
            tr = view.transforms.get_transform('visual', 'document').simplified
            scale = np.linalg.norm((tr.map([1, 0]) - tr.map([0, 0]))[:2])
            view.view_program['u_scale'] = scale
        else:
            view.view_program['u_scale'] = 1

    def _compute_bounds(self, axis, view):
        pos = self._data['a_position']
        if pos is None:
            return None
        if pos.shape[1] > axis:
            return (pos[:, axis].min(), pos[:, axis].max())
        else:
            return (0, 0)
