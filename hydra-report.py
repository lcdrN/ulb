
import sys
import re
import os
import calendar
from distutils.dir_util import copy_tree

sys.path.append('hpc-py')  # Add local lib

import datetime
from datetime import timedelta

import script  # Module with tools for scripts
import tools  # Module with common useful tools
import torque  # Module to process Torque accounting 
import hashlib

PATH_OUTPUT = "report/"
files = None

##################
### Class User ###
##################
class User(object):


    #Constructor
    def __init__(self, name):
        self.name = name
        self.jobs = []
        self.id = 0

    def get_id(self):
        """
        Return a unique ID for user object.

        @rtype:   String
        @return:  the ID based on the date report and user name.
        """
        name = self.name.encode('utf-8')
        job = self.jobs[0].name.encode('utf-8')
        return (self.jobs[0].date.strftime('%Y') + self.jobs[0].date.strftime('%m'))+"_"+str(hashlib.sha224(name).hexdigest() + hashlib.sha224(job).hexdigest())


    def add_Job(self, job):
        """
        Add one job to the list of the user jobs.
 
        This function can be used when reading torque accounting.
 
        @type  job: Job
        @param job: The job to add.
        """
        self.jobs.append(job);

    def number_Jobs(self):
        """
        Return the number of jobs for the user.
 
        @rtype:   number
        @return:  number of jobs.
        """
        return len(self.jobs)

    def get_avg_mem_user(self):
        """
        Return user memory average for all jobs where exit_code = 0.

        @rtype:   number
        @return:  Average (mem).
        """
        avg = 0
        if(len(self.jobs) > 0):
            for job in self.jobs:
                avg = avg + job.get_ratio_mem()
            return avg / len(self.jobs)
        #If there is no job
        else:
            return 0

    def get_total_used_cpu_walltime(self):
        total = 0
        for job in self.jobs:
            total = total + job.get_used_cpu_walltime();
        return total

    def get_avg_walltime_user(self):
        """
        Return user walltime average for all jobs where exit_code = 0.

        @rtype:   number
        @return:  Average (walltime).
        """
        avg = 0
        if(len(self.jobs) > 0):
            for job in self.jobs:
                avg = avg + job.get_ratio_walltime()
            return avg / len(self.jobs)
        #If there is no job
        else:
            return 0


    def get_avg_cpu_walltime_user(self):
        """
        Return user memory average for all jobs where exit_code = 0.

        @rtype:   number
        @return:  Average (mem).
        """
        avg = 0
        if(len(self.jobs) > 0):
            for job in self.jobs:
                avg = avg + job.get_ratio_cpu_walltime()
            return avg / len(self.jobs)
        #If there is no job
        else:
            return 0

    def get_total_requested_walltime(self):
        """
        Returns the total amount of walltime resources requested by the user.

        @rtype:   number
        @return:  Total (Walltime).
        """
        total = 0
        for job in self.jobs:
            total = total + job.requested_walltime
        return total

    def get_total_used_walltime(self):
        """
        Returns the total amount of walltime resources used by the user.

        @rtype:   number
        @return:  Total (Walltime).
        """
        total = 0
        for job in self.jobs:
            #If job exit successfully
            if(job.exit_code == 0):
                total = total + job.used_walltime
        return total

    def get_total_requested_mem(self):
        """
        Returns the total amount of Memory resources requested by the user.

        @rtype:   number
        @return:  Total (Memory).
        """
        total = 0
        for job in self.jobs:
            total = total + job.requested_mem
        return total

    def get_total_used_mem(self):
        """
        Returns the total amount of Memory resources used by the user.

        @rtype:   number
        @return:  Total (Memory).
        """
        total = 0
        for job in self.jobs:
            #If job exit successfully
            if(job.exit_code == 0):
                total = total + job.used_mem
        return total

    def number_by_date(self):
        """
        Return the number of jobs per day.

        @rtype:   dict
        @return:  number of jobs per day (Key : date, value : number of jobs).
        """
        dates = dict()
        for job in self.jobs:
            if not job.date in dates:
                dates[job.date] = 0
            dates[job.date] += 1

        return dates


    def print_number_job_by_date(self, start_date, stop_date):
        """
        Returns the total amount of walltime resources requested by the user.

        This function is used to build the bar chart.

        @type  start_date : Datetime
        @param start_date : Beginning of the period.

        @type  stop_date : Datetime
        @param stop_date : End of the period.

        @rtype:   Array
        @return:  [ [Dates], [Values]].
        """
        interval = calendar.monthrange(stop_date.year,start_date.month)
        last = interval[1]

        start = datetime.date(start_date.year, start_date.month, 1)
        stop = datetime.date(start_date.year, start_date.month, last)
        label = []
        value = []
        dates = self.number_by_date()
        while start <= stop:
            if(start in dates):
                label.append(start.day)
                value.append(dates[start])
            else :
                label.append(start.day)
                value.append(0)
            start = start + timedelta(days=1)
        return [label, value]






    def create_sublist_date(self, queue, queue_name):
        """
        Create a sub-list per date per queue 

        @type  queue : List of jobs
        @param queue : List of jobs of a queue.

        @type  queue_name : String
        @param queue_name : The name of the queue

        @rtype:   String
        @return:  HTML with all sublist for a queue
        """
        job_dates = self.split_job_per_date(queue)
        dates = sorted(job_dates.keys())
        html_file = open("hpc-report/sidebar.html", "r")
        html = html_file.read()
        sublist = ""
        for date in dates:
            job_list = ""
            tmp = ""
            for job in job_dates[date]:
                job_list = job_list + job.print_job_for_list()
            tmp = html.format(str(date.day)+'-'+str(date.month)+'-'+str(date.year)+str(queue_name), job_list, str(date.day)+'/'+str(date.month)+'/'+str(date.year), "date-item")
            sublist += tmp
        return sublist

      
    def split_job_per_date(self, queue):
        """
        Create a dict of job from a queue

        @type  queue : List of jobs
        @param queue : List of jobs of a queue.

        @rtype:   Dict
        @return:  A dict of jobs (Key : Datetime => Jobs)
        """
        job_dates = dict()
        for job in queue:
            if not job.date in job_dates:
                job_dates[job.date] = []
            job_dates[job.date].append(job)
        return job_dates




    def create_sublist(self):
        """
        Return html sidebar with a sublist for each queue.

        @rtype:   String
        @return:  HTML sidebar.
        """
        smp = [x for x in self.jobs if x.queue == "smp"]
        sc = [x for x in self.jobs if x.queue == "single_core"]
        mpi = [x for x in self.jobs if x.queue == "mpi"]
        other = [x for x in self.jobs if x.queue != "smp" and x.queue != "single_core" and x.queue != "mpi"]
        name = ["SMP", "Single Core", "MPI", "Other"]
        i = 0
        sublist = ""

        # for job in other:
        #     job.queue = "Other"



        for queue in [smp, sc, mpi, other]:
            if(len(queue) > 0):
                html_file = open("hpc-report/sidebar.html", "r")
                html = html_file.read()
                # job_list = ""
                # for job in queue:
                #     job_list += job.print_job_for_list()
                html = html.format(queue[0].queue, self.create_sublist_date(queue, i), name[i], "queue")
                sublist += html
            i+=1

        return sublist

    def max_job_mem(self):
        """
        Return the value of the job with the max requested memory.

        @rtype:   number
        @return:  user's requested memory.
        """
        max_job = self.jobs[0];
        for job in self.jobs:
            if job.requested_mem > max_job.requested_mem:
                max_job = job
        return max_job.requested_mem



    def get_scrore(self):
        """
        Return a Score based on ressource usage.

        @rtype:   number
        @return:  user's score.
        """
        score = 0
        for job in self.jobs:
            score += job.score()

        return round(score)


    def generate_line_table(self, path):
        """
        Return HTML table line with performances.

        @rtype:   String
        @return:  HTML table line.
        """
        return """<tr><td>""" + self.name + """
        </td><td> """ + str(self.number_Jobs()) + """
        </td><td> """ + str(len([x for x in self.jobs if x.exit_code == 0])) + """
        </td><td> """ + str(len([x for x in self.jobs if x.exit_code != 0])) + """
        </td><td> """ + str(round(self.get_avg_mem_user()*100)) + """
        </td><td> """ + str(round(self.get_avg_walltime_user()*100)) + """
        </td><td> """ + str(round(self.get_total_used_cpu_walltime())) + """
        </td><td> """ + str(round(self.get_total_requested_mem(), 2)) + """
        </td><td> """ + str(round(self.get_total_used_mem(), 2)) + """
        </td><td> """ + str(round(self.get_total_requested_walltime()/3600, 2)) + """
        </td><td> """ + str(round(self.get_total_used_walltime()/3600, 2)) + """
        </td><td> """ + str(round(self.max_job_mem(), 2)) + """
        </td><td> """ + str(self.get_scrore()) + """
        </td><td> <a href=" """+path+"/"+self.get_id() + """.html"  target="_blank">Report</a></td></tr>"""





##################
#    Class Job   #
##################
class Job(object):

    def __init__(self, job):
        self.name               = job['name']
        self.id                 = job['id']
        self.date               = job['date']
        self.used_mem           = job['used-mem']
        self.requested_mem      = job['requested-mem']
        self.used_walltime      = job['used-walltime']
        self.requested_walltime = job['Resource_List.walltime']
        self.nb_requested_nodes = job['nb-requested-nodes']
        self.nb_requested_cores = job['nb-requested-cores']
        self.nb_cores_allocated = job['nb-cores-allocated']
        self.queue              = job['queue']
        self.exit_code          = job['exit-code']
        self.start_time         = job['start-time']
        self.used_cput          = job['used-cput']
        self.completion_time    = job['completion-time']
        self.queuing_time       = job['queuing-time']

        self.check_job()


        if(self.used_mem > self.requested_mem):
            self.used_mem = self.requested_mem
        if(self.used_walltime > self.requested_walltime):
            self.used_walltime = self.requested_walltime


    def check_job(self):
        if(self.nb_requested_cores < 0 or self.nb_requested_nodes < 0 or self.nb_cores_allocated < 0):
            tools.error("")

        if(type(self.used_mem) is str):
            tools.error("Job : "+ self.id +" the "+ self.date.strftime('%Y') + self.date.strftime('%m')+ self.date.strftime('%d') +" : Error Used Memory")
            self.used_mem = 0

        if(self.used_mem < 0): 
            tools.error("Job : "+ self.id +" : Negative Used Memory")
            self.used_mem = 0

        if(self.used_walltime < 0):
            tools.error("Job : "+ self.id +" : Negative Used Walltime")
            self.used_walltime = 0

        if(self.requested_walltime < 0):
            tools.error("Job : "+ self.id +" : Negative Requested Walltime")
            self.requested_walltime = 0

        if(self.requested_mem < 0):
            tools.error("Job : "+ self.id +" : Negative Requested Mem")
            self.requested_mem = 0

        if(self.name == ""):
            tools.warning("Job without Name")
        if(self.completion_time < self.start_time):
            tools.error("Job : "+ self.id +" : completion time before start time")



    def score(self):
        score = 0
        if(self.exit_code == 0):
            score += (self.used_walltime/3600) - ((self.requested_walltime/3600)/2)
            score += (self.used_mem) - (self.requested_mem/2)
        else:
            score = score - (self.used_walltime/3600)
            score = score - self.used_mem
            score = score - 1
        return score

    def get_ratio_cpu_walltime(self):
        if(self.requested_walltime > 0 and self.nb_requested_cores > 0 and self.exit_code == 0):
            return (self.nb_cores_allocated * self.used_walltime) / (self.nb_requested_cores * self.requested_walltime)
        else:
            return 0

    def get_used_cpu_walltime(self):
        return self.used_walltime*self.nb_cores_allocated

    def get_ratio_mem(self):
        """
        Return ratio between Memory used and Memory resquested.

        @rtype:   number
        @return:  Ratio (Mem used/requested) between 0 and 1.
        """
        if(self.requested_mem > 0 and self.exit_code == 0):
            val = self.used_mem / self.requested_mem
            if(val > 1):
                return 1
            else:
                return val
        else:
            return 0

    def get_ratio_walltime(self):
        """
        Return ratio between Walltime used and Walltime resquested.

        @rtype:   number
        @return:  Ratio (Walltime used/requested) between 0 and 1.
        """
        if(self.requested_walltime > 0 and self.exit_code == 0):
            val = self.used_walltime / self.requested_walltime
            if(val > 1):
                return 1
            else:
                return val
        else:
            return 0

    def print_job_for_list(self):
        """
        Return the HTML representation of the job.

        @rtype:   String
        @return:  HTML <li> of the job.
        """
        if(int(self.exit_code) != 0):
            exit = """<span class="badge badge-primary badge-pill"><i class="fas fa-exclamation-triangle"></i></span>"""
        else:
            exit = ""

        return """<li class="element"><a class="list-ulb
        list-ulb-action d-flex justify-content-between align-items-center"
        id="list-home-list """+ str(id(self)) +"""   " 
        data-toggle="list" 
        href="#list-home" 
        role="tab"
        id_job= """+ str(id(self)) +"""
        exit_code= """ + str(self.exit_code) + """
        queue= """ + str(self.queue) + """ 
        percent_walltime = """ + str(self.get_ratio_walltime()*100) + """
        start_time = """ + str(self.start_time) + """
        end_time = """ + str(self.completion_time) + """
        queuing_time= """+ str(self.queuing_time) +"""
        requested_walltime = """ + str(self.requested_walltime) + """
        used_walltime = """+ str(self.used_walltime) +"""
        requested_mem = """+ str(self.requested_mem) +"""
        used_mem = """+ str(self.used_mem) +"""
        used_cput = """+ str(self.used_cput) +"""
        nb_requested_nodes = """+ str(self.nb_requested_nodes) +"""
        nb_requested_cores = """+ str(self.nb_requested_cores) +"""
        nb_cores_allocated = """+ str(self.nb_cores_allocated) +"""
        title = """ + str(self.id) + """
        aria-controls="home">""" + str(self.name) + exit + """</a></li>"""






############
#   Other  #
############ 
def generate_html_table(users, path):
    html = ""
    for user in users:
        html += users[user].generate_line_table(path) 
    return html




def print_help():
    """ Print help message to console.  """

    print("""
  hydra-report.py [-h | --help] [-o <output file>] [-l <log file>] <Torque accounting files>

  The script extract Torque accounting data and generate HTML report per user with Hydra usage reports.

  Options:
    -h or --help: print this help.
    -o or --output <output file>: specify the repertory name which the HTML reports will be printed. Default "report/"
    -l or --logfile <log file>: specify the file name to which logs (warnings and errors) will be printed.
    
    """)

    return



if __name__ == "__main__":
    # Parse all the files.
    # acc_data = dict with dates as keys and array with jobs as value
    # Get passed args
    script.collect_args()

    # Process args
    if script.is_arg('h') or script.is_arg('help'):
        print_help()
        sys.exit(0)

    if script.is_arg('o'):
        PATH_OUTPUT = script.get_arg('o')[0]
    if script.is_arg('output'):
        PATH_OUTPUT = script.get_arg('output')[0]

    if script.is_arg('l'):
        tools.set_log(script.get_arg('l')[0])
    if script.is_arg('logfile'):
        tools.set_log(script.get_arg('logfile')[0])

    #Get torque accounting files
    files = script.get_arg(None)

    if files == None:
        tools.error('please pass at least one Torque accounting file!')
        print_help()
        sys.exit(1)


    acc_data = torque.parse_accounting(files)


    #Create Object User and Job

    # Handle variation over time
    dates = sorted(acc_data.keys())

    if dates[0].month != dates[-1].month:
        tools.error("More than 1 month selected!")
        print_help()
        sys.exit(1)



    users = dict()

    for date in dates:
        for job in acc_data[date]:
            user = job['user'];
            if(not 'Resource_List.walltime' in job):
                job['Resource_List.walltime'] = 0

            job['date'] = date

            j = Job(job)

            if(not user in users):
                users[user] = User(user)
            
            users[user].add_Job(j)

    #End

    #Create User with all jobs
    general = User('All')
    for user in users:
        general.jobs = general.jobs + users[user].jobs

    users['All'] = general


    #Create repertory if not exist
    if not os.path.exists(PATH_OUTPUT):
        os.makedirs(PATH_OUTPUT)

    if not dates:
        tools.error("No jobs in Torque Accounting file!")
        sys.exit(1)


    #Generate HTML Table
    html_file = open("hpc-report/table.html", "r")
    html = html_file.read()
    file = open(PATH_OUTPUT+"/"+dates[0].strftime('%Y') + dates[0].strftime('%m')+".html", "w")
    file.write(html.format(generate_html_table(users, dates[0].strftime('%Y') + dates[0].strftime('%m')), dates[0].strftime('%Y') + dates[0].strftime('%m')))


    #Copy/Paste Assets (JavaScript)
    copy_tree("hpc-report/assets/", PATH_OUTPUT+"/assets")


    #Create Month repertory
    PATH_OUTPUT = PATH_OUTPUT + "/" + dates[0].strftime('%Y') + dates[0].strftime('%m') + "/"
    if not os.path.exists(PATH_OUTPUT):
        os.makedirs(PATH_OUTPUT)



    html_file = open("hpc-report/index.html", "r")
    html = html_file.read()

    #Genrate HTML Report (user)
    for user_name in users:
        user = users[user_name]
        file = open(PATH_OUTPUT+user.get_id()+".html", "w")
        file.write(html.format(
            user.print_number_job_by_date(dates[0], dates[-1]),
            user.create_sublist(),
            user.name + ' : ' + dates[0].strftime("%B")
            ))

