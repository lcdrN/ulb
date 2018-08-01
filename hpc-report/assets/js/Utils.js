class Utils{



	adapt_metric(used, requested, metric_min, metric_value){
	    var m_r = metric_min
	    var m_u = metric_min

	    used = used * metric_value[0][1];
	    requested = requested * metric_value[0][1];

	    for (var i = 0; i < metric_value.length; i++) {
	        if(used >= metric_value[i][1]){
	            used = used / metric_value[i][1];
	            m_u = metric_value[i][0];
	        }
	        if(requested >= metric_value[i][1]){
	            requested = requested / metric_value[i][1];
	            m_r = metric_value[i][0];
	        }
	    }

	    used = used.toFixed(2);
	    requested = requested.toFixed(2);

	    if(m_r == m_u){
	        return [used, requested + " " + m_r];
	    } else{
	        return [used + " " + m_u, requested + " " + m_r];
	    }

	}	

	getColorForPercentage(value) {
	    //value from 0 to 1
	    var hue=((value)*120).toString(10);
	    return ["hsl(",hue,",50%,50%)"].join("");
	}


	capitalizeFirstLetter(string) {
	    return string.charAt(0).toUpperCase() + string.slice(1);
	}


	write_long_time(time){
		var time_minutes = time;
		var value = [["day(s)", 1440], ["hour(s)", 60], ["minute(s)", 1]];
		var time_txt = "";

		for (var i = 0; i < value.length; i++) {
			var tmp = 0;
			while(time_minutes >= value[i][1]){
				tmp++;
				time_minutes = time_minutes - value[i][1]
			}
			if(tmp >= 1){
				if(time_txt != ""){
					time_txt = time_txt + " and " + tmp + " " + value[i][0];
				}
				else{
					time_txt = tmp + " " + value[i][0];
				}
			}

		}

		return time_txt;
	}


	write_short_time(time){
		var time_minutes = time;
		var value = [["days", 1440], ["hours", 60], ["mins", 1]];
		var time_txt = "";

		for (var i = 0; i < value.length; i++) {
			var tmp = 0;
			while(time_minutes >= value[i][1]){
				tmp++;
				time_minutes = time_minutes - value[i][1]
			}
			if(tmp >= 1){
				return "~" + tmp + " " + value[i][0]
			}

		}

		return "None";
	}


} 
