""" users.py handle users data """

import re
import os
import subprocess
import json
import tools

IS_VSC = re.compile('^vsc(\d+)$')
GET_HOME = re.compile('Directory: ([^\s]+)')
GET_VSC_UNIV = re.compile('/user/([^/]+)/')
IS_ULB = re.compile('/.*ulb.*/')
IS_VUB = re.compile('/.*vub.*/')
IS_SCC = re.compile('/.*scc.*/')
UNKNOWN_USER = re.compile('no such user')

_USERS_CACHE = dict() # Cache processed users

def account_data(username):
    """ Will determine user origin (SISC, VSC or CECI) and
    return a dictionnary with user associated data

    Args:
    username: username

    Returns:
    A dictionnary with information about the user.

    User data dictionnary keys with values: 'username', 'home_dir', 'work_dir', 'ssh_key', 'origin'
    User data dictionnary keys with booleans: 'sisc', 'vsc', 'ceci'
    """

    # Check the cache
    if username in _USERS_CACHE:
        return _USERS_CACHE[username]

    # Init user entry
    user = dict()
    user['username'] = username
    user['univ'] = 'unknown'
    user['group'] = 'unknown'

    # Collect finger data
    if finger(user) == 0:
        user['origin'] = 'unknown'
        user['group'] = username
        user['univ'] = 'unknown'
    elif IS_VSC.match(username) != None:
        user['origin'] = 'vsc'
        user['group'] = username
        matches = GET_VSC_UNIV.match(user['ldap_home'])
        if matches == None:
            tools.warning('failed to extract university for VSC user ' +
                          username + ' from home dir ' + user['ldap_home'])
        else:
            user['univ'] = matches.group(1)
    elif IS_ULB.match(user['home_path']):
        user['univ'] = 'ulb'
        user['origin'] = 'sisc'
    elif IS_VUB.match(user['home_path']):
        user['univ'] = 'vub'
        user['origin'] = 'sisc'
    elif IS_SCC.match(user['home_path']):
        user['univ'] = 'sisc'
        user['origin'] = 'sisc'
    else:
        user['univ'] = 'unknown'
        tools.warning('failed to determine university for user ' + username +
                      ' from home dir ' + user['home_path'])

  # print "Added user ", user['username'], ' - ', user['group']
    global _USERS_CACHE
    _USERS_CACHE[username] = user

    return user

def finger(user):
    """ Execute finger on the passed user entry and return collected data.
    Entry must have ['username'] defined.

    Args:
        user: user name

    Returns:
        1 or 0

    """

    user['ldap_home'] = ''

    # Must use 2.6 style as still in place on mn05
    # finger_cmd = subprocess.Popen(
    #     ["finger", user['username']],
    #     stdout=subprocess.PIPE)
    # output = finger_cmd.stdout.read()
    output = subprocess.check_output(['finger', user['username']], stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
    # print("output = ", output.decode('utf-8'))
    if UNKNOWN_USER.search(output) is not None:
        user['home_path'] = ''
        return 0

    # Extract from output
    matches = GET_HOME.search(output)
    if matches == None:
        tools.warning('failed to extrat home dir for ' +
                      user['username'] + ' in finger output ' + output)
    else:
        user['ldap_home'] = matches.group(1)

    if user['ldap_home'] != '':
        user['home_path'] = os.path.realpath(user['ldap_home'])
    else:
        user['home_path'] = ''

    # print "Got ", user['username'], ' - ', user['ldap_home'], ' - ', user['home_path']

    return 1
