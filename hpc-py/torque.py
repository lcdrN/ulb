""" torque.py handle Torque data """

import re
import fileinput
import datetime
import jobs
import tools

IS_BYTE_SIZE = re.compile('^(\d+)([bkmgt]+)$')
IS_MULTI_NODES = re.compile('\+')
IS_INT = re.compile('^\d+$')
IS_NIC = re.compile('^nic\d+$')
IS_WALLTIME = re.compile('walltime')
IS_HMS = re.compile('^\d+:\d+')
GET_DATA_PAIR = re.compile('^([^=]+)=(.+)')
GET_DATE = re.compile('^(\d+)/(\d+)/(\d+)$')
GET_PPN = re.compile('^ppn=(\d+)$')
GET_HOST_DATA = re.compile('^([^/]+)/(.*)')
GET_CORES_PART = re.compile('^(\d+)-(\d+)$')

# Correspondance between Torque and script job parameters
_TORQUE_JOB = {
    'jobname': 'name',
    'ctime': 'creation-time',
    'qtime': 'queuing-time',
    'etime': 'xxx-time',
    'start': 'start-time',
    'end': 'completion-time',
    'Resource_List.mem': 'requested-mem',
    'Resource_List.nodect': 'nb-reserved-nodes',
    'Resource_List.neednodes': 'requested-features',
    'Resource_List.nodes': 'requested-resources',
    'session': 'process-id',
    'total_execution_slots': 'nb-cores-allocated',
    'unique_node_count': 'nb-unique-nodes',
    'Exit_status': 'exit-code',
    'resources_used.cput': 'used-cput',
    'resources_used.energy_used': 'power-consumption',
    'resources_used.mem': 'used-mem',
    'resources_used.vmem': 'used-vmem',
    'resources_used.walltime': 'used-walltime',
    'exec_host': 'running-hosts'
}

def parse_accounting(files):
    """ Load the content of an accounting file

    Args:
    files: array of file names

    Returns:
    A dictionnary with dates (days) as key and as value an array
    with dictionnaries holding jobs data.

    """

    # global IS_BYTE_SIZE, IS_MULTI_NODES, IS_INT, GET_DATE, GET_DATA_PAIR, IS_WALLTIME, _TORQUE_JOB

    acc_data = dict()

    # Iterate on every line of every file
    for line in fileinput.input(files):
        # Data separator is space (quite stupid though)
        data = line.split(' ')
        if len(data) < 2:
            tools.error('got invalid accounting line ' + line +
                        ' from ' + fileinput.filename() + '. Skipped.')
            continue

        date = data.pop(0) # Remove date from the list
        # print fileinput.filename(), " - date = ", date
        tmp = data.pop(0) # Remove job combined data entry

        # print fileinput.filename(), " - tmp = ", tmp

        # Second (combined) entry has the accounting time part + job status and user data
        tmp_data = tmp.split(';')

        # print "tmp_data = ", tmp_data

        # Keep only completed jobs which has logically the 'E' flag...
        if tmp_data[1] != 'E':
            continue

        # Build job entry
        job = jobs.new_job()
        job['accounting-time'] = tmp_data[0] # Accounting time
        job['status'] = tmp_data[1] # Job status
        job['id'] = tmp_data[2] # Job ID

        # Add user data in main list
        data.append(tmp_data[3])

        # Process jobs data
        for entry in data:
            matches = GET_DATA_PAIR.match(entry)
            key = matches.group(1)
            val = matches.group(2)

            # print key, ' = ', val

            # Got a size?
            matches = IS_BYTE_SIZE.match(val)
            if matches:
                # print "Converting ", matches.group(1), ' - ', matches.group(2)
                # Convert whatever size in GB
                val = tools.size_convert(matches.group(1), matches.group(2), 'gb')

            # Got exec_host?
            if key == 'exec_host' and IS_MULTI_NODES.search(val):
                _extract_exec_host(val, job)
            elif key == 'Resource_List.neednodes':
                matches = IS_INT.match(val)
                # If just asked node(s)
                if matches != None:
                    job['nb-requested-nodes'] = int(val)
                    job['nb-requested-cores'] = job['nb-requested-nodes'] * job['nb-requested-nodes']
                elif IS_MULTI_NODES.search(val): # If multiple nodes/ppn/resources
                    res_parts = str(val).split('+')
                    for part in res_parts:
                        _extract_compute_resources(part, job)
                else: # Case with just x node(s) and ppn
                    _extract_compute_resources(val, job)
            elif IS_WALLTIME.search(key):
                val = tools.get_seconds(val)
            elif key == 'resources_used.cput' and IS_HMS.match(val):
                # print "Converting ", val, " to seconds."
                val = tools.get_seconds(val)


            # print key, ' = ', val

            # Convert str to int when needed
            if isinstance(val, str) is True and IS_INT.match(val) is not None:
                val = int(val)

            # Keep that pair, convert Torque key to std job key
            if key in _TORQUE_JOB:
                job[_TORQUE_JOB[key]] = val
            else:
                job[key] = val

        # print 'Job ', job['id'], ' - ', job['user']

        # Complete the data
        if job['completion-time'] == 0:
            tools.warning('found job ' + job['id'] + ' without execution time in file ' + fileinput.filename())
            job['is-invalid'] = True
            job['used-cput'] = 0
            job['used-walltime'] = 0
            job['time-spent-queue'] = 0
            job['cpu-walltime'] = 0
        else:
            job['cpu-walltime'] = job['used-walltime'] * job['nb-requested-cores']
            # time when job was queued = exec time minus time added
            # in the queue in seconds
            job['time-spent-queue'] = job['start-time'] - job['queuing-time']

        # print "Got cput and nb-requested-cores as ", job['used-cput']
        # print "Got nb-requested-cores as ",  job['nb-requested-cores']

        # Torque date is not ISO 8610, fix that
        matches = GET_DATE.match(date)
        if matches not None:
            date_obj = datetime.date(int(matches.group(3)), int(matches.group(1)), int(matches.group(2)))
            job['date'] = date_obj
            if date_obj not in acc_data:
                acc_data[date_obj] = []

            acc_data[date_obj].append(job)

    return acc_data

def _extract_compute_resources(req_res, job):
    """ Extract all the details from the job requested resources.

    Args:
        req_res: requested resources
        job: job object

    Returns:
        seconds

    """

    # global IS_NIC, GET_PPN, IS_INT

    res_parts = req_res.split(':')
    if len(res_parts) == 1:
        job['nb-requested-nodes'] += 1
        job['nb-requested-cores'] += 1
        job['invalid-requested-resources'] = True
        tools.warning('found invalid requested compute resources: ' + req_res +
                      ' for job ' + job['id'] + ' in file ' + fileinput.filename())
    else:
        # print 'Req res: ', val, ' nodes =  ', res_parts[0], ' - cores = ', res_parts[1]
        # Get requested node(s)
        if IS_NIC.match(res_parts[0]) is not None:
            job['nb-requested-nodes'] += 1
        elif IS_INT.match(res_parts[0]) is not None:
            job['nb-requested-nodes'] += int(res_parts[0])
        else:
            tools.warning("couldn't determine requested node resource from: " +
                          req_res + ' for job ' + job['id'] + ' by user ' + job['user'],
                          ' in file ' + fileinput.filename() + '. Job skipped.')

        # Get requested core(s)
        matches = GET_PPN.match(res_parts[1])
        nb_cores = 1
        req_feat = ''
        if matches is None:
            req_feat = res_parts[1] # Case neednodes=1:gpgpu
        else:
            nb_cores = int(matches.group(1))
            try:
                req_feat = res_parts[2]
            except IndexError:
                req_feat = ''

        job['nb-requested-cores'] += job['nb-requested-nodes'] * nb_cores
        job['requested-features'].append(req_feat)

    return

def _extract_exec_host(hosts_str, job):
    """ Extract list of hosts that executed the job.

    Args:
        time: string in [hh:[mm:]]ss

    Returns:
        seconds

    """

    # global GET_HOST_DATA, GET_CORES_PART, IS_INT

    hosts = dict()
    hlist = hosts_str.split('+')
    # Loop on the hosts
    for host in hlist:
        # Extract name and associated cores
        matches = GET_HOST_DATA.match(host)
        name = matches.group(1)
        cores = matches.group(2)

        # Single core?
        if IS_INT.match(cores) is not None:
            cores_list = [int(cores)]
        else:
            # Extract list of cores/ranges
            parts = cores.split(',')
            cores_list = []
            for part in parts:
                # One specific core in the list?
                if IS_INT.match(part) is not None:
                    cores_list.append(int(part))
                else:
                    # Get the range
                    crange = GET_CORES_PART.match(part)

                    # Fill the list
                    start = int(crange.group(1))
                    end = int(crange.group(2)) + 1
                    for core in range(start, end):
                        cores_list.append(core)
            # End core parts loop

        # Associate host name and allocated cores
        hosts[name] = cores_list

    # Associate the exec hosts to the job
    job['running-hosts'] = hosts

    return
