from lib.services.config import get_const

# Color list for node types
COLOR_LIST = [(1.0, 0.8941176, 0.7686275),
                (0.545098, 0.5372549, 0.5372549),
                (1.0, 0.9803922, 0.8039216),
                (0.9019608, 0.9019608, 0.9803922),
                (0.1921569, 0.3098039, 0.3098039),
                (0.3921569, 0.5843137, 0.9294118),
                (0.0, 0.0, 0.8039216),
                (0.0, 0.7490196, 1.0),
                (0.2745098, 0.5098039, 0.7058824),
                (0.2509804, 0.8784314, 0.8156863),
                (0.0, 0.3921569, 0.0),
                (0.4980392, 1.0, 0.0),
                (0.1960784, 0.8039216, 0.1960784),
                (0.4196078, 0.5568627, 0.1372549),
                (1.0, 1.0, 0.0),
                (0.854902, 0.6470588, 0.1254902),
                (0.8039216, 0.3607843, 0.3607843),
                (0.9568627, 0.6431373, 0.3764706),
                (0.6980392, 0.1333333, 0.1333333),
                (0.9803922, 0.5019608, 0.4470588),
                (1.0, 0.0, 0.0),
                (1.0, 0.0784314, 0.5764706),
                (0.7294118, 0.3333333, 0.827451),
                (0.5411765, 0.1686275, 0.8862745),
                (0.5764706, 0.4392157, 0.8588235)]

# TODO: Get these constants by making a config function
COLUMN_TYPES = get_const('columntypes')
# {'n_id': 'int', 'n_label': 'qstr', 'n_type': 'qstr', 'e_weight': 'int', 'e_from': 'int', 'e_to': 'int', '-': '', 'e_id': 'int', 'e_label': 'qstr', 'e_type': 'qstr'}

ALGS = get_const('alg')

FLABELS = get_const('forcelabels')

NODECNAMES = get_const('nodecnames')

EDGECNAMES = get_const('edgecnames')

UNIFIEDCNAMES = NODECNAMES + EDGECNAMES
# MARKERSIZE = get_const('size')
