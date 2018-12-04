import configparser
import globals

def read_cfg_file(filename):
    """
        read_cfg_file()

        Read the config file <filename>.

        PARAMETER : (str)filename

        RETURNED VALUE : (bool_success, configparser.ConfigParser object)
    """
    success = True
    errors = []
    cfgini = configparser.ConfigParser()

    try:
        cfgini.read(filename)
    except configparser.DuplicateOptionError as err:
        success = False
        errors.append("Ill-formed config file '{0}' : {1}".format(filename, err))

    if success:
        try:
            # let's check the presence of some values :
            _ = cfgini["output.console"]
            _ = cfgini["output.console"]["invert_rtltext"]
            _ = cfgini["pipeline.trace"]
            _ = cfgini["pipeline.trace"]["yes"]
            _ = cfgini["pipeline.trace"]["no"]
            _ = cfgini["pipeline.use FB1D-FB4F chars"]
        except KeyError as err:
            success = False
            errors.append("Ill-formed config file '{0}' : {1}".format(filename, err))

    if success:
        globals.RTL_SYMBOLS = (cfgini["inputdata.format"]["RTL_SYMBOL_START"],
                               cfgini["inputdata.format"]["RTL_SYMBOL_END"])
        globals.RTLREADER_REGEX = globals.create_rtlreader_regex()

    return success, errors, cfgini

# should be initialized by read_cfg_file()
CFGINI = None