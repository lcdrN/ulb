""" tools.py offers a number of tools reusable in any script/lib """

import math
import sys

_CONVERTION_TABLE = dict()
_CONVERTION_TABLE['b'] = 1
_CONVERTION_TABLE['kb'] = 1000
_CONVERTION_TABLE['kib'] = 1024
_CONVERTION_TABLE['mb'] = math.pow(1000, 2)
_CONVERTION_TABLE['mib'] = math.pow(1024, 2)
_CONVERTION_TABLE['gb'] = math.pow(1000, 3)
_CONVERTION_TABLE['gib'] = math.pow(1024, 3)
_CONVERTION_TABLE['tb'] = math.pow(1000, 4)
_CONVERTION_TABLE['tib'] = math.pow(1024, 4)
_CONVERTION_TABLE['pb'] = math.pow(1000, 5)
_CONVERTION_TABLE['pib'] = math.pow(1024, 5)

_FOUT = sys.stdout # To handle output writes
_FLOG = sys.stderr # To handle log writes

def size_convert(val, unit, target_unit='b'):
    """ Convert a size to a different unit

    Args:
        val: value
        unit: its unit (b, kb, mb, kib, mib etc)
        target_unit: optional target unit, default to bytes ('b')

    Returns:
        The value converted into the target unit.

    """

    val = float(val) # Work with reals

    if target_unit not in _CONVERTION_TABLE:
        return 0

    conv_val = (val * _CONVERTION_TABLE[unit]) / _CONVERTION_TABLE[target_unit]

    return conv_val

def get_seconds(time):
    """ Convert time in [hh:[mm:]ss]] into seconds.

    Args:
        time: string in [hh:[mm:]]ss

    Returns:
        seconds

    """

    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(time.split(":"))))

def set_output(fname=None):
    """ Set the file pointer where to write the output.

    Args:
        fname: if passed, will be used as file name, stdout otherwise

    Returns:
        seconds

    """

    global _FOUT

    if fname and fname != '-':
        _FOUT = open(fname, 'w')
    else:
        _FOUT = sys.stdout

    return 1

def set_log(fname=None):
    """ Set the log file. If fname is passed, the log file will be created under
    the passed name. Otherwise sys.stderr will be used.

    Args:
        fname: file name

    Returns:
        Always 1.

    """

    global _FLOG

    if fname and fname != '-':
        _FLOG = open(fname, 'w')
    else:
        _FLOG = sys.stderr

    return 1

def write_out(string):
    """ Write passed string to the output.

    Args:
        string: text string

    Returns:
        Always 1.

    """

    # global _FOUT

    print(string, file=_FOUT)

    return 1

def write_log(string):
    """ Write passed string to the log.

    Args:
        string: text string

    Returns:
        Always 1.

    """

    print(string, file=_FLOG)

    return

def error(string):
    """ Write passed string to the log as an error message.

    Args:
        string: text string

    Returns:
        Always 1.

    """

    write_log('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    write_log('!! Error: ' + string)
    write_log('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    return

def warning(string):
    """ Write passed string to the log as an warning message.

    Args:
        string: text string

    Returns:
        Always 1.

    """

    write_log('================================================================================')
    write_log('== Warning: ' + string)
    write_log('================================================================================')

    return
