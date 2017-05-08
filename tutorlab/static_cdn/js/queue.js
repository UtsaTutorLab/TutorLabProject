var pusher = new Pusher('f3826192229bfe688efd', {
      encrypted: true
    });

var channel = pusher.subscribe('ch1');
channel.bind('enqueue', function(data) {
    	update_queue();
    	});      

var counter = 0;


function update_queue() {
	$('#sidebar-wrapper').load('../ta_tutor/ #sidebar-wrapper');
	cur_student = $("#upnext").data("nextstudent")
	cur_classID = $("#upnext").data("nextclass")
}

function queue_formfill(){
	$('.nav-tabs a[href="#menu1"]').tab('show')
	document.getElementById('student').value = $('#upnext').data('nextstudent');
	document.getElementById('classID').value = $('#upnext').data('nextclass');
}