import sys
import datetime
import logging.config
from functools import wraps
from django.conf import settings

"""
Notes: Order of logs

    1. loglevel = debug,    it will log (debug,info,warn,error,critical) statements
    2. loglevel = info,     it will log (info,warn,error,critical) statements
    3. loglevel = warn,     it will log (warn,error,critical) statements
    4. loglevel = error,    it will log (error,critical) statements
    5. loglevel = critical, it will log (critical) statements

    logger.debug("Something debug")
    logger.info("It works.")
    logger.warn("Something not ideal")
    logger.error("Something went wrong")
"""

def createLogger(logHandler):
    logger = logging.getLogger(logHandler)
    logger = setLoggerLevel(logger,settings.APP_LOGGING_LEVEL)
    return logger

def setLoggerLevel(logger,loglevel):
    if loglevel == "DEBUG":
        logger.setLevel(logging.DEBUG)
    if loglevel == "INFO":
        logger.setLevel(logging.INFO)
    if loglevel == "WARN":
        logger.setLevel(logging.WARN)
    if loglevel == "ERROR":
        logger.setLevel(logging.ERROR)
    if loglevel == "CRITICAL":
        logger.setLevel(logging.CRITICAL)
    return logger


def functionlogs(log='app'):
    def wrap(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(log)
            function.__class__
            file_name = function.__code__.co_filename.rsplit("/", 1)
            if file_name and len(file_name)>1:
                file_name = file_name[1]
            init_time = datetime.datetime.now()
            logger.info("*******Starting function %s : %s" % (file_name, function.__qualname__))
            # if settings.APP_LOGGER_FUNCTION_IN_PARAMS.upper() == 'TRUE':
            #     logger.debug("I/P: with args={} kwargs={}".format(args, kwargs))
            try:
                response = function(*args, **kwargs)
            except Exception as error:
                logger.error("Function '{}' raised {} with error '{}'".format(function.__qualname__,error.__class__.__name__,str(error)))
                raise error
            # if settings.APP_LOGGER_FUNCTION_OUT_PARAMS.upper() == 'TRUE':
            #     logger.debug("O/P: {}".format(response))
            end_time = datetime.datetime.now()
            logger.info("*******Finished function %s : %s in %s seconds" % (file_name, function.__qualname__,end_time-init_time))
            return response
        return wrapper
    return wrap

def exceptionlogs(e,log='app'):
    '''
        exception_traceback[0]="ErrorType"      Example: <type 'exceptions.ZeroDivisionError'>
        exception_traceback[1]="Error"          Example: ZeroDivisionError('integer division or modulo by zero')
        exception_traceback[2]="ErrorObject"    Example: <traceback object at 0x7f9f45039fc8>
    '''
    exception_traceback = sys.exc_info()
    logger = logging.getLogger(log)
    logger.error('-'*80)
    logger.error('Error Type   : %s' %(exception_traceback[0]))
    logger.error('Error Trace  : %s' %(exception_traceback[1]))
    logger.error('Error Line: %s %s' %(exception_traceback[2].tb_lineno,e))
    logger.error('-'*80)


def _setmsg(success_msg,error_msg, flag):
    '''construct and return success or error messages based on the flag
    success_msg : success message
    error_msg : error message
    flag : result flag'''
    msg=''
    if flag:
        msg = success_msg
    else:
        msg = error_msg
    return flag, msg
