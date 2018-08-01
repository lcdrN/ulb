""" script.py offers a number of tools useful in scripts like cmd line arguments management """

# Imports
import re
import sys

# Global variables
_HYD_NOVAL = '_noval_'
_HYD_NOOPT = '_noopt_'
_HYD_ARGS = dict()
_HYD_IS_OPT = re.compile('^\-\-?(.+)')

# Collect arguments from the command line
def collect_args():
    """ collect the command line arguments from sys.argv
    Options are recognised if they start with a dash (-) or double dash (--)

    Returns:
    dict with the options and their values (as array).
    Key '_HYD_NOVAL' is used if no option associated with a value.

    """

    # Rm script name
    sys.argv.pop(0)

    # Default cmd line option
    key = _HYD_NOOPT

    global _HYD_ARGS
    _HYD_ARGS[_HYD_NOOPT] = _HYD_NOVAL # Init for arguments wihout options

    # Iterate on the args
    for item in sys.argv:
        # Option?
        matches = _HYD_IS_OPT.match(item)

        if matches:
            # Keep it
            key = matches.group(1)

            # print "Got option ", key

        # Check if already seen & set default value
        if key not in _HYD_ARGS:
            _HYD_ARGS[key] = _HYD_NOVAL

            # Pass to next argument
            continue

        # First assigned value?
        if _HYD_ARGS[key] == _HYD_NOVAL:
            _HYD_ARGS[key] = []

        # We are in value(s) after the option, check if option already used
        _HYD_ARGS[key].append(item)
        # print "add ", item, " to ", key

        # Reset to default option
        key = _HYD_NOOPT

    return _HYD_ARGS

# ----------------------------------------------------------------

def is_arg(opt):
    """Pass an option argument (-input or input for instance).
    Return 1 if argument option was catched, 0 if not."""

    matches = _HYD_IS_OPT.match(opt)
    if matches:
        opt = matches.group(1)

    if opt in _HYD_ARGS:
        return 1

    return 0

# ----------------------------------------------------------------

def get_arg(opt):
    """Pass an option argument (-input or input for instance) and get back the value.
    No argument to the fct returns the values collected without an option before them."""

    if opt == None:
        opt = _HYD_NOOPT
    else:
        matches = _HYD_IS_OPT.match(opt)
        if matches:
            opt = matches.group(1)

    if opt in _HYD_ARGS:
        if _HYD_ARGS[opt] == _HYD_NOVAL:
            return None

        return _HYD_ARGS[opt]
    else:
        return None
