class Job{

	/**
	 * Create a new Job
	 * 
	 * @constructor
	 * @this {Job}
	 * @param {elem} elem HTML element with data.
	 */
    constructor(elem){
        this.id_job =             elem.attr("id_job");
        this.html =               elem;
        this.queuing_time=        elem.attr("queuing_time");
        this.queue=        		  elem.attr("queue");
        this.start_time =         elem.attr("start_time");
        this.requested_walltime = Number(elem.attr("requested_walltime"))/3600;
        this.end_time=            elem.attr("end_time");
        this.nb_requested_nodes=  Number(elem.attr("nb_requested_nodes"));
        this.nb_requested_cores=  Number(elem.attr("nb_requested_cores"));
        this.nb_cores_allocated=  elem.attr("nb_cores_allocated");
        this.percent_walltime=    elem.attr("percent_walltime");
        this.requested_mem =      Number(elem.attr("requested_mem"));
        this.used_mem=            Number(elem.attr("used_mem"));
        this.used_walltime =      Number(elem.attr("used_walltime"))/3600;
        this.exit_code =          Number(elem.attr("exit_code"));
        this.used_cput =          Number(elem.attr("used_cput"))/3600;
        this.id_acc=              elem.attr("title");
        this.job_name=            elem.text();
    }


    /**
	 * Get Walltime Average for the job
	 * 
	 * @return {Number} Walltime average (0-100)
	 */
    get_avg_walltime(){
        if(this.requested_walltime.toFixed(2) == 0){
            return 0
        }else{
            return ((this.used_walltime / this.requested_walltime)*100).toFixed(0);
        }
    }

    /**
	 * Get Memory Average for the job
	 * 
	 * @return {Number} Memory average (0-100)
	 */
    get_avg_mem(){
        if(this.requested_mem.toFixed(2) == 0){
            return 0
        }else{
            return ((this.used_mem / this.requested_mem)*100).toFixed(0);
        }
    }

    get_eff_walltime(){
        if((this.used_walltime * this.nb_requested_cores).toFixed(2) == 0){
            return 0
        } else{
            return ((this.used_cput / (this.used_walltime * this.nb_requested_cores) )*100).toFixed(0);
        }
    }
} 
