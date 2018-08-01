""" jobs.py provides data structures and management for HPC jobs """

def new_job():
    """ Create and return an empty job data structure

    Returns:
    A dictionary with jobs structure

    """

    job = dict()
    job['name'] = ''
    job['creation-time'] = 0
    job['queuing-time'] = 0
    job['execution-time'] = 0
    job['completion-time'] = 0
    job['accounting-time'] = 0
    job['time-spent-queue'] = 0
    job['requested-mem'] = 0
    job['nb-reserved-nodes'] = 0
    job['requested-features'] = []
    job['process-id'] = 0
    job['nb-cores-allocated'] = 0
    job['nb-unique-nodes'] = 0
    job['exit-code'] = 0
    job['used-cput'] = 0
    job['power-consumption'] = 0.0
    job['used-mem'] = 0.0
    job['used-vmem'] = 0.0
    job['used-walltime'] = 0
    job['requested-resources'] = ''
    job['status'] = 'unknown' # Job status
    job['id'] = 'noId' # Job ID
    job['invalid-requested-resources'] = False # Flag to 1 if got invalid requested resources
    job['is-invalid'] = False # Flag to 1 is job is invalid
    job['nb-requested-nodes'] = 0
    job['nb-requested-cores'] = 0
    job['running-hosts'] = dict()

    return job
