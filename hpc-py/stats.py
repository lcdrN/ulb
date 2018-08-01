""" stats.py provides data structures and management for HPC statistics """

import re
import datetime
import users

_STAT_FIELDS = ['nb-jobs', 'nb-selected-jobs', 'nb-requested-nodes',
                'nb-requested-cores',
                'used-cput', 'used-walltime', 'cpu-walltime', 'requested-mem',
                'used-mem', 'time-spent-queue']
_FILTERS = None
#             5m   10m   30m   1h    2h     5h     12h    24h   48h      3d       4d     5d
_QUEUE_TIME_BINS = [300, 600, 1800, 3600, 7200, 18000, 43200, 86400, 172800, 259200, 345600, 432000]
IS_STAR = re.compile('\*')


def new_stats():
    """ Create and init a dict to store job stats

    Returns:
        A dict with a structure used in various stat modules.

    """

    stats = {
        'global': init_fields(),
        'smp': init_fields(),
        'sc': init_fields(),
        'mpi': init_fields(),
        'users': dict(),
        'groups': dict(),
        'univs': dict(),
        'nodes': dict(),
        'queuing': {
            'global': {
                'queuingtime': 0
            },
            'frequencies': dict(),
            'dates': dict(),
            'users': dict(),
        },
        'efficiencies': dict()
    }

    return stats


def init_fields(data=None):
    """ Get a dict and init predefined list of keys from _STAT_FIELDS to zero

    Returns:
        Passed or new dict with a predefined keys set to 0.

    """

    if data is None:
        data = dict()

    for field in _STAT_FIELDS:
        data[field] = 0

    return data


def collect_general_stats(job, stats, field='global'):
    """ Collect general stats.

    Args:
        job: job entry
        stats: stats dict to hold the data
        field: define wich field in stats dict, default to 'global'

    Returns:
        1 or 0

    """

    item = stats[field]
    item['nb-jobs'] += 1
    if job['is-invalid'] is True:
        return

    if filter_job(job) == False:
        job['is-invalid'] = True  # Don't continue to work with this job
        return

    # print('Proc job ', job['id'], ' - ', job['user'], ' - ', job['used-cput'])
    item['nb-selected-jobs'] += 1
    item['used-cput'] += job['used-cput']
    item['nb-requested-nodes'] += job['nb-requested-nodes']
    item['nb-requested-cores'] += job['nb-requested-cores']
    item['used-walltime'] += job['used-walltime']
    item['cpu-walltime'] += job['cpu-walltime']
    item['requested-mem'] += job['requested-mem']
    item['used-mem'] += job['used-mem']
    item['time-spent-queue'] += job['time-spent-queue']

    return


def collect_users_stats(job, stats):
    """ Collect user stats from the passed job.

    Args:
        job: job entry
        stats: dict with users stats

    Returns:
        1 or 0

    """

    if job['is-invalid'] is True:
        return

    user_acc = users.account_data(job['user'])

    # Do user stats
    if job['user'] not in stats['users']:
        # stats['users'][job['user']] = dict()
        # user = stats['users'][job['user']]
        # user['account'] = user_acc
        # user['id'] = job['user']
        # user['group'] = job['group']
        # user['univ'] = user_acc['univ']
        # init_fields(user)
        # # user['nb-jobs'] = 0
        # user['nb-sc-jobs'] = 0
        # user['nb-smp-jobs'] = 0
        # user['nb-mpi-jobs'] = 0

        stats['users'][job['user']] = {
            'account': user_acc,
            'id': job['user'],
            'group': job['group'],
            'univ': user_acc['univ'],
            'nb-sc-jobs': 0,
            'nb-smp-jobs': 0,
            'nb-mpi-jobs': 0
        }
        init_fields(stats['users'][job['user']])

    user = stats['users'][job['user']]

    user['nb-jobs'] += 1
    if job['nb-requested-nodes'] == 1 and job['nb-requested-cores'] == 1:
        user['nb-sc-jobs'] += 1
    elif job['nb-requested-nodes'] == 1:
        user['nb-smp-jobs'] += 1
    else:
        user['nb-mpi-jobs'] += 1

    user['used-cput'] += job['used-cput']
    user['used-walltime'] += job['used-walltime']

    # print("Job - user ", job['user'], ' - ', job['id'], ' with ', job['cpu-walltime'])
    user['cpu-walltime'] += job['cpu-walltime']
    user['requested-mem'] += job['requested-mem']
    user['used-mem'] += job['used-mem']
    user['time-spent-queue'] += job['time-spent-queue']

    # Do group stats
    if job['group'] not in stats['groups']:
        stats['groups'][job['group']] = {
            'id': job['group'],
            'univ': user_acc['univ'],
            'nb-sc-jobs': 0,
            'nb-smp-jobs': 0,
            'nb-mpi-jobs': 0
        }
        init_fields(stats['groups'][job['group']])

    group = stats['groups'][job['group']]

    group['nb-jobs'] += 1
    if job['nb-requested-nodes'] == 1 and job['nb-requested-cores'] == 1:
        group['nb-sc-jobs'] += 1
    elif job['nb-requested-nodes'] == 1:
        group['nb-smp-jobs'] += 1
    else:
        group['nb-mpi-jobs'] += 1

    group['used-cput'] += job['used-cput']
    group['used-walltime'] += job['used-walltime']
    group['cpu-walltime'] += job['cpu-walltime']
    group['requested-mem'] += job['requested-mem']
    group['used-mem'] += job['used-mem']
    group['time-spent-queue'] += job['time-spent-queue']

    return


def collect_univ_stats(job, stats):
    """ Collect stats on universities distribution.

    Args:
        job: job entry
        stats: stats dict to hold the data

    Returns:
        1 or 0

    """

    if job['is-invalid'] is True:
        return

    user_acc = users.account_data(job['user'])

    univ_id = user_acc['univ']

    if univ_id not in stats['univs']:
        stats['univs'][univ_id] = {
            'id': univ_id,
            'nb-sc-jobs': 0,
            'nb-smp-jobs': 0,
            'nb-mpi-jobs': 0
        }
        init_fields(stats['univs'][univ_id])

    univ = stats['univs'][univ_id]

    univ['nb-jobs'] += 1
    if job['nb-requested-nodes'] == 1 and job['nb-requested-cores'] == 1:
        univ['nb-sc-jobs'] += 1
    elif job['nb-requested-nodes'] == 1:
        univ['nb-smp-jobs'] += 1
    else:
        univ['nb-mpi-jobs'] += 1

    univ['used-cput'] += job['used-cput']
    univ['used-walltime'] += job['used-walltime']
    univ['cpu-walltime'] += job['cpu-walltime']
    univ['requested-mem'] += job['requested-mem']
    univ['used-mem'] += job['used-mem']
    univ['time-spent-queue'] += job['time-spent-queue']

    return


def collect_queuing_stats(job, stats):
    """ Collect stats on queuing times.

    Args:
        job: job entry
        stats: stats dict to hold the data

    Returns:
        1 or 0

    """

    if job['is-invalid'] is True:
        return

    # Pick the bin
    bin_val = 0
    for bin_step in _QUEUE_TIME_BINS:
        if job['time-spent-queue'] <= bin_step:
            bin_val = bin_step
            break
    if bin_val == 0:
        bin_val = 432001

    if bin_val not in stats['queuing']['frequencies']:
        stats['queuing']['frequencies'][bin_val] = 0
    if job['date'].isoformat() not in stats['queuing']['dates']:
        stats['queuing']['dates'][job['date'].isoformat()] = []
    if job['user'] not in stats['queuing']['users']:
        stats['queuing']['users'][job['user']] = []

    stats['queuing']['frequencies'][bin_val] += 1
    stats['queuing']['dates'][job['date'].isoformat()].append(job['time-spent-queue'])
    stats['queuing']['users'][job['user']].append(job['time-spent-queue'])
    stats['queuing']['global']['queuingtime'] += job['time-spent-queue']

    return


def collect_efficiencies_stats(stats, accounting_data, daily_nodes):
    """ Collect stats on cluster efficiencies.

    Args:
        stats: stats dict to hold the data
        accounting_data: jobs daily accounting
        daily_nodes: nodes available per day

    Returns:
        1 or 0

    """

    # Global efficiencies
    stats['efficiencies']['walltime'] = float(
        stats['global']['used-cput']) / stats['global']['cpu-walltime']
    stats['efficiencies']['memory'] = float(
        stats['global']['used-mem']) / stats['global']['requested-mem']

    stats['efficiencies']['daily'] = dict()
    stats['efficiencies']['global'] = dict()
    # stats['efficiencies']['global']['wasted-cores'] = 0

    time_bin = 3600  # Time range in seconds to bin cluster usage

    # Fill occupancy data for all the processed days
    nodes_occup = dict()  # Hold occupancy data per day
    for date in accounting_data:
        for job in accounting_data[date]:
            fill_cluster_occupancy(job, nodes_occup, time_bin)

    # Get efficiencies now
    tot_clust_efficiency = 0
    tot_cores_efficiency = 0
    tot_mem_efficiency = 0
    tot_cores_over_commit = 0
    tot_mem_over_commit = 0

    for date_time in accounting_data:
        date = date_time.strftime("%Y-%m-%d")
        # print("Daily stats for ", date)

        # Get computing resources available for that day
        tot_nodes_cores = 0
        tot_modes_mem = 0
        for node_name in daily_nodes[date]:
            node = daily_nodes[date][node_name]
            tot_nodes_cores += node['np']
            tot_modes_mem += node['mem']

        # print("Nb cores on ", date, ' = ', tot_nodes_cores)

        # Build daily stat from occupancy stats
        stats['efficiencies']['daily'][date] = {
            'cores-available': tot_nodes_cores,
            'mem-available': tot_modes_mem,
            'cores-requested': 0,
            'cores-used': 0,
            'mem-requested': 0,
            'mem-used': 0,
            'cluster-efficiency': 0,
            'cores-efficiency': 0,
            'mem-efficiency': 0,
            'cores-overcommit': 0,
            'mem-overcommit': 0
        }
        daily_stat = stats['efficiencies']['daily'][date]
        count = 0

        for occup_data in nodes_occup[date]:
            # print("Occ data for ", date, ' - ', count, ' = ', occup_data)

            daily_stat['cores-used'] += occup_data['nb-used-cores']
            cores_effic = float(occup_data['nb-used-cores']) / tot_nodes_cores
            mem_effic = float(occup_data['used-mem']) / tot_modes_mem
            daily_stat['cores-efficiency'] += cores_effic
            daily_stat['mem-efficiency'] += mem_effic

            if mem_effic > cores_effic:
                clust_effic = mem_effic
            else:
                clust_effic = cores_effic

            daily_stat['cluster-efficiency'] += clust_effic

            # Over commitments from the jobs
            daily_stat['cores-requested'] += occup_data['nb-requested-cores']

            if occup_data['nb-requested-cores'] > tot_nodes_cores:
                over_val = occup_data['nb-requested-cores'] - tot_nodes_cores
                # print("For date ", date, ' - bin ', count, ' cores over commit of ',
                # over_val, ' cores-overcommit now = ', daily_stat['cores-overcommit'])
                daily_stat['cores-overcommit'] += over_val

            daily_stat['mem-requested'] += occup_data['requested-mem']
            daily_stat['mem-used'] += occup_data['used-mem']

            if occup_data['requested-mem'] > tot_modes_mem:
                over_val = occup_data['requested-mem'] - tot_modes_mem
                daily_stat['mem-overcommit'] += over_val
                # print("For date ", date, ' - bin ', count, ' mem over commit of ',
                # over_val, ' mem-overcommit now = ', daily_stat['mem-overcommit'])

            count += 1

        tot_clust_efficiency += daily_stat['cluster-efficiency']
        tot_cores_efficiency += daily_stat['cores-efficiency']
        tot_mem_efficiency += daily_stat['mem-efficiency']
        tot_cores_over_commit += daily_stat['cores-overcommit']
        tot_mem_over_commit += daily_stat['mem-overcommit']

        # Calc averages
        nb_occ_data = len(nodes_occup[date])
        daily_stat['cores-used'] /= nb_occ_data
        daily_stat['cores-requested'] /= nb_occ_data
        daily_stat['mem-used'] /= nb_occ_data
        daily_stat['mem-requested'] /= nb_occ_data
        daily_stat['cluster-efficiency'] /= nb_occ_data
        daily_stat['cores-efficiency'] /= nb_occ_data
        daily_stat['mem-efficiency'] /= nb_occ_data
        # print("Final cores over commit = ", daily_stat['cores-overcommit'], ' ->
        # ', daily_stat['cores-overcommit'] / nb_occ_data)
        daily_stat['cores-overcommit'] /= nb_occ_data
        # print("Final mem over commit = ", daily_stat['mem-overcommit'], ' -> ',
        # daily_stat['mem-overcommit'] / nb_occ_data)
        daily_stat['mem-overcommit'] /= nb_occ_data

    return 1


def fill_cluster_occupancy(job, nodes_occup, time_bin):
    """ Fill the nodes occupancy covered by the passed job.

    Args:
        job: job entry
        nodes_occup: occupancy data for the nodes
        time_bin: time intervals

    Returns:
        1 or 0

    """

    # print("Filling occupancy for job ", job['id'], ' - walltime ', job['used-walltime'])

    # Get the start date and time
    startdate_time = datetime.datetime.fromtimestamp(int(job['start-time']))
    enddate_time = datetime.datetime.fromtimestamp(int(job['completion-time']))
    # Work with faull days
    diff_start = startdate_time.replace(hour=0, minute=0, second=0, microsecond=0)
    diff_end = enddate_time.replace(hour=23, minute=59, second=59, microsecond=999999)
    diff = diff_end - diff_start
    # Get the number of days between the 2
    nb_days = diff.days + 1

    # print('-> times: start = ', startdate_time.isoformat(), ' - end = ',
    # enddate_time.isoformat(), ' - nb job days = ', nb_days)

    # Cover the days
    for day_step in range(nb_days):
        today = startdate_time.strftime("%Y-%m-%d")
        # print('  -> filling for ', today)

        if today in nodes_occup:
            occup_data = nodes_occup[today]
        else:
            # Initialise the data
            occup_data = []

            nb_bin_steps = int(86400 / time_bin)
            for bin_pos in range(nb_bin_steps):
                occup_bin = {
                    'nb-jobs': 0,
                    'nb-requested-cores': 0,
                    'nb-used-cores': 0,
                    'requested-mem': 0,
                    'used-mem': 0
                }
                occup_data.append(occup_bin)

            # Keep occupancy data for processed day
            nodes_occup[today] = occup_data

        # Get nb of seconds of start time from beginning of the day
        day_start = startdate_time.replace(hour=0, minute=0, second=0, microsecond=0)
        # Nb of seconds between starting day and job start time
        start_seconds = (startdate_time - day_start).seconds
        # Get nb of seconds between start and end times
        nb_seconds = (enddate_time - startdate_time).seconds
        if nb_seconds + start_seconds > 86400:  # We are above one full day
            # Keep seconds between nb of seconds of starting day and end of the day
            nb_seconds = 86400 - start_seconds

        # Prepare range to fill occupancy data
        start_bin = int(start_seconds / time_bin)
        if startdate_time.strftime("%Y-%m-%d") != enddate_time.strftime("%Y-%m-%d"):
            # If end date is not start date, fill bins of current day to the end
            end_bin = int(86400 / time_bin)
        else:
            end_bin = int(nb_seconds / time_bin) + 1


        for bin_step in range(start_bin, end_bin):
            occup_bin = occup_data[bin_step]
            occup_bin['nb-jobs'] += 1
            occup_bin['nb-requested-cores'] += job['nb-requested-cores']
            occup_bin['nb-used-cores'] += job['nb-cores-allocated']
            occup_bin['requested-mem'] += job['requested-mem']
            occup_bin['used-mem'] += job['used-mem']

        # Move to next day
        startdate_time = startdate_time + datetime.timedelta(days=1)
        # if startdate_time.strftime("%Y-%m-%d") != enddate_time.strftime("%Y-%m-%d"):
        # If the next day is not the job end date, set H:M:S to 0
        startdate_time = startdate_time.replace(hour=0, minute=0, second=0, microsecond=0)

    return 1


def filter_job(job):
    """ Filter a job and return True to keep it, False to skip it

    Args:
        job: job data structure

    Returns:
        True if passed the filters, False if not
    """

    # Get the filters
    filters = job_filters()

    if filters == None:
        return True

    keep = True  # Keep the node by default

    if 'mandatory-queues' in filters:
        keep = False
        for item in filters['mandatory-queues']:
            if item in job['queue']:
                keep = True
                break
            if keep == True:
                break  # Stop here if node kept

        if not keep:
            return False  # Return if job not selected

    if 'exclude-queues' in filters:
        for item in filters['exclude-queues']:
            if item in job['queue']:
                return False  # Return as job not selected

    if 'mandatory-user-origins' in filters:
        keep = False
        user_acc = users.account_data(job['user'])
        for item in filters['mandatory-user-origins']:
            if item in user_acc['univ']:
                keep = True
                break
            if keep == True:
                break  # Stop here if node kept

        if not keep:
            return False  # Return if job not selected

    if 'exclude-user-origins' in filters:
        user_acc = users.account_data(job['user'])
        for item in filters['exclude-user-origins']:
            if item in user_acc['univ']:
                return False  # Return as job not selected

    return True


def job_filters(filters=None):
    """ Get/set job filtes.

    Args:
        filters: to set if passed

    Returns:
        job filters

    """

    global _FILTERS

    if filters != None:
        _FILTERS = filters

    return _FILTERS
