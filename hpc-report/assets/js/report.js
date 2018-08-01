var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
var months = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"];

var DATA = {
    WALLTIME : "walltime",
    MEMORY : "memory"
}
var METRIC = {
    HOURS : "Hours",
    GB    : "GB"
}
var ICON = {
    WALLTIME : "far fa-clock",
    MEMORY : "far fa-hdd",
    TERMINAL : "fas fa-terminal",
    MPI : "fas fa-code-branch",
    SC : "fas fa-genderless",
    SMP : "fas fa-sitemap",
    OTHER : "far fa-handshake",
    WAIT  : "fas fa-stopwatch",
    SUCCESS : "fas fa-check-circle"
}

var QUEUE = {
    SMP : "SMP",
    MPI : "MPI",
    SC  : "SINGLE_CORE"
}



// Value --> Message
var exit_code_message = {"0":     "Job execution successful",
                        "-1":     "Job execution failed, before files, no retry",
                        "-2":     "Job execution failed, after files, no retry",
                        "-3":     "Job execution failed, do retry",
                        "-4":     "Job aborted on MOM initialization",
                        "-5":     "Job aborted on MOM init, no migrate",
                        "-6":     "Job aborted on MOM init, ok migrate",
                        "-7":     "Job restart failed",
                        "-8":     "Exec() of user command failed",
                        "-9":     "Could not create/open stdout stderr files",
                        "-10":    "Job exceeded a memory limit",
                        "-11":    "Job exceeded a walltime limit",
                        "-12":    "Job exceeded a CPU time limit",
                        "-13":    "Could not create the job's cgroups",
                        "-14":    "Prologue failed"
    };


Array.prototype.diff = function(a) {
    return this.filter(function(i) {return a.indexOf(i) < 0;});
};



//When HTML page is loaded
$(document).ready(function() {

     $('#switcher-lg').prop('checked', true);


    //Set Title
    $('#title').text($('#title').attr("date")+" report");

    var system = new System();
    system.init_home();

    //Use Key down and key up to naviguate in jobs list
    use_key(system);

    //Search bar
    search();

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
    });


    $('#switcher-lg').on('change', function() {
        if (!$(this).is(':checked')) {
            system.set_all(false);
            $('#title_average').text("Average of resources used by successful jobs all the resources requested");
            system.init_home();
        }else{
            system.set_all(true);
            $('#title_average').text("Average of resources used by all the jobs over all the resources requested");
            system.init_home();
        }
    });


    $('.link_job').click(function(e) {
        elem = e.target;
        system.load_job($(elem));
        $('#job').show();
        $('#home').hide();
        removeActive();
        var job = system.get_job($(elem).text()  + " - " + $(elem).attr("title"));
        $(job.html).addClass('active');

    });


	$('.list-ulb').click(function(e) {
	    e.preventDefault();
        removeActive();
        if($(e.target).hasClass('list-ulb')){
          var  p = $(e.target);
		  system.load_job($(e.target));
          $(e.target).addClass('active');
        } else{
            p = $(e.target).parent();
            if($(p).hasClass('list-ulb')){
                system.load_job($(p));
                $(p).addClass('active');
            }
            else{
                p = $(p).parent();
                system.load_job($(p));
                $(p).addClass('active');
            }
        }

        $('#job').show();
        $('#home').hide();
        $($('#jobs_tab').children()[0]).addClass('active');
        $($('#home_tab').children()[0]).removeClass('active');
	});

    $('#home_tab').click(function(e) {
        $('#job').hide();
        $('#home').show(); 
        $($('#jobs_tab').children()[0]).removeClass('active');
        $($('#home_tab').children()[0]).addClass('active');
        $('#title').text($('#title').attr("date")+" report");   
    });

});


function search(){
    $("#search").on("keyup", function() {
        var input, filter, ul, li, a, i;
        input = document.getElementById('search');
        filter = input.value.toUpperCase();
        li = document.getElementsByClassName('element');
        nav = document.getElementsByClassName('date-item');

        for (i = 0; i < li.length; i++) {
            a = li[i].getElementsByTagName("a")[0];
            if (a.innerHTML.toUpperCase().indexOf(filter) > -1 || $(a).attr("title").indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }

        for (i = 0; i < nav.length; i++){
            li = nav[i].getElementsByTagName("ul")[0].getElementsByTagName("li");
            if (li.length === $(li).filter(function () { return $(this).css('display') === 'none';}).length){
                nav[i].style.display = 'none';
                $(nav[i].getElementsByTagName("ul")[0]).find("a").toggle();
            }
            else{
                nav[i].style.display = '';
                $(nav[i].getElementsByTagName("ul")[0]).find("a").toggle();
                console.log($(nav[i]).find("a"))
            }

        }
        
    });
}

function removeActive(){
    $('a.active').removeClass('active');
}



function use_key(system){

    document.addEventListener("keydown", function(e) {
        if(e.keyCode == 40) {
            var a = $(".list-ulb-action:visible");
            for (var i = 0; i < a.length; i++) {
                if($(a[i]).hasClass('active') && i+1 < a.length){
                    $(a[i]).removeClass('active');
                    $(a[i+1]).addClass('active');
                    system.load_job($(a[i+1])); 
                    break;
                }
            }
        }
        else if(e.keyCode == 38) {
            var a = $(".list-ulb-action:visible");
            for (var i = 0; i < a.length; i++) {
                if($(a[i]).hasClass('active') && i-1 >= 0){
                    $(a[i]).removeClass('active');
                    $(a[i-1]).addClass('active');
                    system.load_job($(a[i-1])); 
                    break;
                }
            }
        }
    });
}



