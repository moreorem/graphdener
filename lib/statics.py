from lib.services.config import (get_const, get_attr, get_importer)
COLUMN_TYPES = get_const('columntypes')

ALGS = get_const('alg')

FLABELS = get_const('forcelabels')

NODECNAMES = get_const('nodecnames')

EDGECNAMES = get_const('edgecnames')

MARKER_SIZE = get_attr('marker_size')

ARROWHEAD_SIZE = get_attr('arrow_size')

ACCEPTED_SYMBOLS = get_importer('acceptedsymbols')
