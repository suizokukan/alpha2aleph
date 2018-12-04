import logging
import cfgini

class LoggerPlus(logging.Logger):
    """
        LoggerPlus class
    """
    def __init__(self, name, level=logging.NOTSET):
        """
                LoggerPlus.__init__()
        """
        logging.Logger.__init__(self, name, level)

    def pipelinetrace(self, pipeline_part, msg, *args, **kwargs):
        """
                LoggerPlus.pipelinetrace()

                Call Logger.info() only if the flags defined in the cfg file
                authorize a log message.
        """
        if pipeline_part in cfgini.CFGINI["pipeline.trace"]["yes"]:
            return logging.Logger.info(self, "["+pipeline_part+"] "+msg, *args, **kwargs)

        elif not pipeline_part in cfgini.CFGINI["pipeline.trace"]["no"]:
            raise RuntimeError("Undefined pipeline part '%s'.", pipeline_part)

        return None

logging.setLoggerClass(LoggerPlus)
LOGGERFORMAT = '%(levelname)-8s %(message)s'
logging.basicConfig(format=LOGGERFORMAT, level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)
