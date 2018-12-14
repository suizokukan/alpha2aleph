import re
import alpha2aleph.globalsrtl

LOGGER = alpha2aleph.glob.LOGGER

def get_rtlreader_regex():
    if alpha2aleph.globalsrtl.RTL_SYMBOLS[0] == alpha2aleph.globalsrtl.RTL_SYMBOLS[1]:
        res = '{0}(?P<rtltext>[^{0}]*){0}'.format(re.escape(RTL_SYMBOLS[0]))
    else:
        res = '{0}(?P<rtltext>[^{0}{1}]*){1}'.format(re.escape(alpha2aleph.globalsrtl.RTL_SYMBOLS[0]),
                                                     re.escape(alpha2aleph.globalsrtl.RTL_SYMBOLS[1]))

    alpha2aleph.glob.LOGGER.debug("[D01] new RTLREADER_REGEX : %s", res)

    return re.compile(res)