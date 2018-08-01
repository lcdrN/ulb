class System{


 	/**
	 * Create a new System
	 * 
	 * @constructor
	 * @this {System}
	 */
    constructor(){
        var elements = $('[queue]').get();
        this.jobs = [];
        this.view = new View();
        this.utils = new Utils();
        this.all = true;

        for (var i = 0; i < elements.length; i++) {
            this.jobs.push(new Job($(elements[i])));
            //$(elements[i]).text(this.reduce_text($(elements[i]).text()))
        }

	    this.smp = this.job_per_queue(this.jobs, QUEUE.SMP);
	    this.sc = this.job_per_queue(this.jobs, QUEUE.SC);
	    this.mpi = this.job_per_queue(this.jobs, QUEUE.MPI);
	    this.other = this.jobs.diff(this.smp).diff(this.sc).diff(this.mpi);

	    for (var i = 0; i < this.jobs.length; i++) {
	    	this.jobs[i].queue = this.utils.capitalizeFirstLetter(this.jobs[i].queue);
	    }


	    this.all_queue = this.groupBy(this.jobs, "queue");


        this.view.reSize(this.jobs);


    }

    groupBy(arr, property) {
		  return arr.reduce(function(memo, x) {
		    if (!memo[x[property]]) { memo[x[property]] = []; }
		    memo[x[property]].push(x);
		    return memo;
		  }, {});
	}


	get_average_memory(){
		return this.total_requested_mem() / this.jobs.length;
	}

	get_average_walltime(){
		return this.total_requested_walltime() / this.jobs.length;
	}

	get_average_efficiency(){
		return this.get_total_requested_walltime_core() / this.jobs.length;
	}



    set_all(value){
    	this.all = value;
    }



     /**
     * Get a job with id
     * 
     * @param {Number} id job's id.
     *
     * @return {Job} job The job.
     */ 
    get_job(id){
    	return this.jobs.filter(function(job) {return job.id_job == id;})[0];
    }

    get_total_used_cput(){
    	var total = 0;
    	this.jobs.forEach(function(job){
    			total += job.used_cput;
    	});
    	return total;
    }


    get_total_requested_walltime_core(){
    	var total = 0;
    	this.jobs.forEach(function(job){
    			total += job.used_walltime*job.nb_requested_cores;
    	});
    	return total;
    }

    /**
     * Get total requested memory
     *
     * @return {number} Get total requested memory
     */ 
    total_requested_mem(){
    	var total = 0;
    	this.jobs.forEach(function(job){
    			total += job.requested_mem
    	});
    	return total;
    }


    /**
     * Get total used memory (where job exit == 0)
     *
     * @return {number} Get total used memory
     */ 
    total_used_mem(){
    	var total = 0;
    	var value = this.all;
    	this.jobs.forEach(function(job){
    		if(!value){
	    		if(job.exit_code == 0){
	    			total += job.used_mem
	    		}
	    	}else{
	    		total += job.used_mem;
	    	}
    	});
    	return total;
    }

    /**
     * Get total requested walltime
     *
     * @return {number} Get total requested walltime
     */ 
    total_requested_walltime(){
    	var total = 0;
    	this.jobs.forEach(function(job){
    		total += job.requested_walltime
    	});
    	return total;
    }

    /**
     * Get total used walltime (where exit code == 0)
     *
     * @return {number} Get total used walltime
     */ 
    total_used_walltime(){
		var total = 0;
		var value = this.all;
		this.jobs.forEach(function(job){
			if(!value){
				if(job.exit_code == 0){
					total += job.used_walltime
				}
			}else{
				total += job.used_walltime
			}
		});
		return total;
    }


    /**
     * Load a job on screen
     *
     * @param {elem} elem Html element of the job
     */ 
    load_job(elem){
    	this.view.load_job(this.jobs.filter(function(job) {return job.id_job == elem.attr("id_job");})[0]);
    }

    /**
     * Init first page on screen
     */ 
    init_home(){

    	var best_worst = this.print_worst_best();


	    
	    var counter = {"row" : [
	    	this.view.init_counter("Memory Average", this.total_requested_mem(), this.total_used_mem(), DATA.MEMORY, 0, best_worst[0], this.get_average_memory(), "Used/Requested"),
	        this.view.init_counter("Walltime Average", this.total_requested_walltime(), this.total_used_walltime(), DATA.WALLTIME, 0, best_worst[1], this.get_average_walltime()*60, "Used/Requested"),
	        this.view.init_counter("Core Usage", this.get_total_requested_walltime_core(), this.get_total_used_cput() , DATA.WALLTIME, 0, best_worst[2], this.get_average_efficiency()*60, "Used/Allocated")]
	    }


	    var label = JSON.parse($("#pluginChart").attr("value"))[0];
	    var value = JSON.parse($("#pluginChart").attr("value"))[1];

	    var chart = { "row": [this.view.init_chart("Jobs started this month", label, value)]}



	    this.home_card();
	    this.view.draw_card('plugin', counter, 4);
	    this.view.draw_card('pluginChart', chart, 12);
    }


    /**
     * Get job  in specific queue
     *
     * @param {Jobs[]} jobs A set of jobs.
     * @param {string} queue The queue. 
     *
     * @return {Job[]} A list of Jobs
     */ 
    job_per_queue(jobs, queue){
        var tab = [];
        this.jobs.forEach(function(job){
            if(job.queue == queue.toLowerCase()){
                tab.push(job);
            }
        });
        return tab;
    }


    /**
     *  Init card of home page
     */ 
    home_card(){

    	var card = { "row" : []};
	    
    	for(var queue in this.all_queue){
    		card.row.push(this.view.init_small_card(queue, this.all_queue[queue].length, this.get_icon(queue), this.Suc_fail(this.number_exit(this.all_queue[queue])[0], this.number_exit(this.all_queue[queue])[1]), null, null, null));
    	}
	    this.view.draw_card('num', card, 4);

	}

	get_icon(queue){
		if(queue == "Smp"){
			return ICON.SMP;
		}
		else if(queue == "Single_core"){
			return ICON.SC
		}
		else if(queue == "Mpi"){
			return ICON.MPI;
		}
		else{
			return ICON.OTHER;
		}
	}



	Suc_fail(success, failed){

	    var footer = "<div title=\"Jobs Succeeded\"><i class=\"fas fa-check-circle\" style=\"color:"+( (success > 0 || failed > 0) ? "green" : "" ) +"\"></i> : " + success + "</div> &emsp; &emsp; &emsp; &emsp;";
	    footer += "<div title=\"Jobs Failed\"><i class=\"fas fa-times-circle\" style=\"color:"+( (success > 0 || failed > 0) ? "red" : "" ) +"\"></i> : " + failed + "</div>";

	    return footer;
	}

	print_worst_best(){
		var stat = this.worst_best();

		return [
			"<i class=\"fas fa-chart-line\" style=\"color:green\"></i> : <a class=\"link_job\" title="+stat[0].job_name+" id_job="+stat[0].id_job+">" + this.reduce_text(stat[0].job_name) + "</a> --> " + stat[0].get_avg_mem() + "%" + "<br>" +
			"<i class=\"fas fa-chart-line\" style=\"color:red\"></i> : <a class=\"link_job\" title="+stat[1].job_name+" id_job="+stat[1].id_job+">" + this.reduce_text(stat[1].job_name) + "</a> --> " + stat[1].get_avg_mem() + "%",
			"<i class=\"fas fa-chart-line\" style=\"color:green\"></i> : <a class=\"link_job\" title="+stat[2].job_name+" id_job="+stat[2].id_job+">" + this.reduce_text(stat[2].job_name) + "</a> --> " + stat[2].get_avg_walltime() + "%" + "<br>" +
			"<i class=\"fas fa-chart-line\" style=\"color:red\"></i> : <a class=\"link_job\" title="+stat[3].job_name+" id_job="+stat[3].id_job+">" + this.reduce_text(stat[3].job_name) + "</a> --> " + stat[3].get_avg_walltime() + "%",
			"<i class=\"fas fa-chart-line\" style=\"color:green\"></i> : <a class=\"link_job\" title="+stat[4].job_name+" id_job="+stat[4].id_job+">" + this.reduce_text(stat[4].job_name) + "</a> --> " + stat[4].get_eff_walltime() + "%" + "<br>" +
			"<i class=\"fas fa-chart-line\" style=\"color:red\"></i> : <a class=\"link_job\" title="+stat[5].job_name+" id_job="+stat[5].id_job+">" + this.reduce_text(stat[5].job_name) + "</a> --> " + stat[5].get_eff_walltime() + "%"
			]

	}


	reduce_text(text){
		if(text.length > 25){
			return text.substring(0, 25)+"...";
		}
		return text
	}


	worst_best(){
		return [
	    this.jobs.reduce(function(l, e) {return (Number(e.get_avg_mem()) > Number(l.get_avg_mem()) && e.exit_code == 0) ? e : l;}),
	    this.jobs.reduce(function(l, e) {return (Number(e.get_avg_mem()) < Number(l.get_avg_mem())  && e.exit_code == 0) ? e : l;}),
	    this.jobs.reduce(function(l, e) {return (Number(e.get_avg_walltime()) > Number(l.get_avg_walltime()) && e.exit_code == 0) ? e : l;}),
	    this.jobs.reduce(function(l, e) {return (Number(e.get_avg_walltime()) < Number(l.get_avg_walltime()) && e.exit_code == 0) ? e : l;}),
	    this.jobs.reduce(function(l, e) {return (Number(e.get_eff_walltime()) > Number(l.get_eff_walltime()) && e.exit_code == 0) ? e : l;}),
	    this.jobs.reduce(function(l, e) {return (Number(e.get_eff_walltime()) < Number(l.get_eff_walltime()) && e.exit_code == 0) ? e : l;})
	    ]
	    
	}



    /**
     * 
     * @param {queue} A set of jobs
     *
     * @return {Number[]} Tab with the number of success jobs and failed jobs
     */ 
	number_exit(queue){
	    var success = 0;
	    var failed = 0;
	    queue.forEach(function(job){
	        if(job.exit_code != 0){
	            failed++;
	        }else{
	            success++;
	        }
	    });
	    return [success, failed];

	}


}
 
