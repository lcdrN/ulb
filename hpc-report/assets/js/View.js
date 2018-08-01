var metric_value_walltime = [["Hours", 60], ["Days", 24], ["Years", 365]]
var metric_value_mem = [["GB", 1000]]


 class View{


 	/**
	 * Create a new View
	 * 
	 * @constructor
	 * @this {View}
	 */
    constructor(){
        //load icon (sidebar)
        feather.replace();
        this.utils = new Utils();
    }


    /**
     * Resize text from HTML sidebar if is too long
     * 
     * @param {Array[Job]} jobs The set of jobs.
     */ 
    reSize(jobs){
        for(var id in jobs){
            var elem = jobs[id].html;
            var textLength = $(elem).text().length;

            if(textLength > 30) {
                elem.css('font-size', '10px');
            } else if(textLength > 20) {
                elem.css('font-size', '13px');
            }
        }
    }


    /**
     * Draw a set of cards
     * 
     * @param {string} id Name of the set.
     * @param {json} json Set of cards.
     * @param {number} size Size of one card.
     */ 
    draw_card(id, json, size){
        if(json.row.length > 0){
        	$("#"+id).empty().removeData();
            materialCards.initialize(id ,null, 'No data found',null,null,null,false, json, size);
        }
    }

    /**
     * Initialize small card
     * 
     * @param {string} title Title of the card.
     * @param {number} value Value to print.
     * @param {string} icon Icon to print.
     * @param {string} footer Footer to print.
     *
     * @return {json} Row with small card's parameters
     */ 
    init_small_card(title, value, icon, footer){

        var row = {
            "CARD_TYPE": "icon",
            "CARD_ICON": icon,
            "CARD_ICON_COLOR": null,
            "CARD_HEADER_STYLE": null,
            "CARD_TITLE": title,
            "CARD_VALUE": value,
            "CARD_FOOTER": footer,
            "CARD_LINK": null
        }

        return row;

    }



    /**
     * Initialize row for counter card
     * 
     * @param {string} title Title of the card.
     * @param {number} requested Requested ressources.
     * @param {number} used Used ressources.
     * @param {string} element WALLTIME or MEMORY.
     * @param {number} exit_code Job's exit code.
     * @param {string} footer Job's footer to load (can be null)
     *
     * @return {json} Row with counter card's parameters
     */ 
    init_counter(title, requested, used, element, exit_code, footer, average, infos){
        var color = "background:grey";
        var icon;
        var metric;
        if(requested <= 0.009){
        	var value = 0;
        }else{
        	var value = ((used / requested)*100).toFixed(0);
        }
        var card_value = "";


        if(exit_code == 0){
            color = "background: linear-gradient(60deg, "+this.utils.getColorForPercentage(value/100 - 0.1)+", "+this.utils.getColorForPercentage(value/100 + 0.1)+");"
        }


        if(element == DATA.WALLTIME){
            icon = ICON.WALLTIME;
            metric = METRIC.HOURS;
            used = this.utils.adapt_metric(used, requested, "Mins", metric_value_walltime)[0];
            requested = this.utils.adapt_metric(used, requested, "Mins", metric_value_walltime)[1];
            card_value = used + "/" + requested;
            if(average != null){
            	card_value = card_value + '<br>' + "<h4 title=\"Requested Average\"> " + this.utils.write_short_time(Math.round(average, 1)) + " per job</h4>";
            }
            if(footer == null){
            	if(title == "Core Usage"){
            		footer = "You used about " + used + " of the " + requested + " allocated";
            	} else{
            		footer = "You used about " + used + " of the " + requested + " requested";
            	}
            }
        }
        else{
        	// requested = Math.round(requested, 2)
        	// used = Math.round(used, 2)
            icon = ICON.MEMORY;
            metric = METRIC.GB;
            used = this.utils.adapt_metric(used, requested, "Mo", metric_value_mem)[0];
            requested = this.utils.adapt_metric(used, requested, "Mo", metric_value_mem)[1];

            card_value =used + '/' + requested
            if(average != null){
            	card_value = card_value + '<br>' + "<h4 title=\"Requested Average\"> ~ " + Math.round(average, 2) + "GB per job</h4>";
            }
            if(footer == null){
            	footer = "You used about " + used + " of the "+ requested + " requested";
            }
        }

        requested = Math.round(requested)
        used = Math.round(used)


        var row = {
            "CARD_TYPE": "chart-pie",
            "CARD_ICON": "fa-external-link",
            "CARD_ICON_COLOR": null,
            "CARD_HEADER_STYLE": color,
            "CARD_TITLE": title,
            "CARD_VALUE": card_value,
            "CARD_FOOTER": footer,
            "CARD_INFOS" : infos,
            "CARD_CHART_DATA": {
                labels: [value+'%'],
                series: [value]
            },
            "CARD_CHART_CONFIG": {donut: true,
                donutWidth: 20,
                startAngle: 0,
                sliceWidth: 7,
                total: 100,
                showLabel: false,
                plugins: [
                    Chartist.plugins.fillDonut({
                        items: [{
                            content: '<h6>'+value+'<span class="small">%</span></h6>',
                            position: 'bottom',
                            offsetY : 20,
                            offsetX: 0
                        }, {
                            content: '<h3><i class="'+icon+'"></i></h3>'
                        }]
                    })
                ]}
            }

        return row
    }

    /**
     * Initialize row for chart card 
     * 
     * @param {string} title Title of the chart.
     * @param {Array[string]} label Label for X axis.
     * @param {Array[number]} value Value for Y axis.
     *
     * @return {json} Row with chart card's parameters
     */ 
    init_chart(title, label, value){

        var number_job = 0;
        for(var i=0;i<value.length;i++){
            number_job = number_job + parseInt(value[i]);
        }

        var row = {
            "CARD_TYPE": "chart-bar",
            "CARD_ICON": "fa-external-link",
            "CARD_ICON_COLOR": null,
            "CARD_HEADER_STYLE": "background: hsl(206, 50%, 60%);",
            "CARD_TITLE": title,
            "CARD_VALUE": "Total : " + number_job+" Jobs",
            "CARD_FOOTER": null,
            "CARD_CHART_DATA": {
                labels: label,
                series: [value]
            },
            "CARD_CHART_CONFIG": {            
                plugins: [
                    Chartist.plugins.tooltip()
                ]
            }
        }

        return row

    }

    /**
     * Load a job on Screen.
     * 
     * @param {Job} job The job to load.
     */ 
    load_job(job){

        //Init row for counter
        var counter = {"row" : [
                this.init_counter("Memory Usage", job.requested_mem, job.used_mem, DATA.MEMORY, job.exit_code, null, null, "Used/Requested") ,
                this.init_counter("Walltime Usage", job.requested_walltime, job.used_walltime, DATA.WALLTIME, job.exit_code, null, null, "Used/Requested")
            ]
        }

        //if(job.queue != QUEUE.SC && job.nb_requested_cores != job.nb_cores_allocated){
           counter.row.push(this.init_counter("Core Usage", job.used_walltime*job.nb_requested_cores, job.used_cput, DATA.WALLTIME, job.exit_code, null, null, "Used/Allocated")); 
        //}


        $('#title').text(job.job_name +" - "+ job.id_acc);  

        var value = "";
        if(job.exit_code == 0){
            value = "Succeeded";
        }
        else{
            value = "Failed";
        }


        var time_start = new Date(job.start_time*1000);
        var time_queue = new Date(job.queuing_time*1000);
        var minutes = (((time_start.getTime() - time_queue.getTime()) / 1000) / 60).toFixed(0) ;


        var message = exit_code_message[job.exit_code]
        if(message == null){
            message = "Job exited with code " + job.exit_code;
        }

        var card = { "row" : [this.init_small_card("Program", value, ICON.TERMINAL, message),
                               this.init_small_card("Nodes", job.nb_requested_nodes, ICON.MPI, job.nb_requested_nodes+" requested"),
                               this.init_small_card("Cores allocated", job.nb_cores_allocated, ICON.SC, job.nb_cores_allocated+" allocated"),
                               this.init_small_card("Time in queue", this.utils.write_short_time(minutes), ICON.WAIT, this.utils.write_long_time(minutes))
                    ]}


        //Draw small card
        this.draw_card('smallcard', card, 3);
        //Draw counter
        this.draw_card('plugin_usage', counter, 12/counter.row.length)
        //Draw Timeline
        this.load_timeline(job);


    }



     /**
     * Load a job's timeline on Screen.
     * 
     * @param {Job} job The job to load.
     */
    load_timeline(job){

        var date_end = new Date(job.start_time*1000)
        date_end.setTime(date_end.getTime() + (job.requested_walltime*3600*1000));

        var dates = [new Date(job.start_time*1000), new Date(job.end_time*1000), date_end];

        for (var i = 0; i < dates.length; i++) {
            $('.Day').get(i).firstChild.data = days[dates[i].getDay()];
            $('.MonthYear').get(i).firstChild.data = months[dates[i].getMonth()] + " " +  (1900+dates[i].getYear());
            $('.DayDigit').get(i).firstChild.data = dates[i].getDate();
            var ampm = dates[i].getHours() >= 12 ? 'PM' : 'AM';
            var minutes = dates[i].getMinutes() >= 10 ? dates[i].getMinutes() : '0' + dates[i].getMinutes();
            var hour = dates[i].getHours().toString() + " : " + minutes;
            $('.time, .time2')[i].innerHTML = hour + " " + ampm;
        }

        var p_walltime = (job.used_walltime/job.requested_walltime)*1000

        $('#dist').width((p_walltime)+'%');
        $('#dist2').width(1000 - (p_walltime)+'%');
        $('#d').attr("x2", (p_walltime)+'em');
        $('#d2').attr("x2", 1000 - (p_walltime)+'%');

    }


    
    


}
