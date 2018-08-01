
$(document).ready(function() {

var title = $('#general').attr('value');


var table = $('table').DataTable( {
	colReorder: true,
    paging: false,
    responsive : true,
    dom: 'Bfrtip',
        buttons: [
            {
                extend: 'pdfHtml5',                
                orientation: 'landscape',
                pageSize: 'LEGAL',
                title: title,
                exportOptions: {
                    columns: [0,1,2,3,4,5,6,7,8,9,10]
                }
            },
        	{
                extend: 'csvHtml5',
                title: title
            },'columnsToggle'
        ]
     
} );
  



});