var pusher = new Pusher('4a389ab4ef763883473e', { 
    	encrypted: true,
    });

var channel = pusher.subscribe('ch1');
channel.bind('enqueue', function(data) {
    update_queue();
});      

var appt_ch = pusher.subscribe('appt'); //channel
appt_ch.bind('new', function(data) { //event 
	update_appt();
});

var note_ch = pusher.subscribe('notify');
note_ch.bind('notes', function(data) {
	update_notify();
});

var post_ch = pusher.subscribe('post_view');
post_ch.bind('comments', function(data) {
	update_post_view();
});

var tutor_admin = pusher.subscribe('admin_view');
tutor_admin.bind('admin_view', function(data){
	update_tutor_admin_view();
});

// var app_ch = pusher.subscribe('presence-Session');
// app_ch.bind('updateQueue', function(data){

// })

function update_tutor_admin_view(){
	$('#my-list-group').load(document.URL + ' #my-list-group');
	document.getElementById("issue_input").value = "";
}

function update_queue() {
	$('#queue').load(document.URL + ' #queue');
}

function update_appt() {
	$('#tutorAccordion').load(document.URL + ' #tutorAccordion');
	$('#tutorTabs').load(document.URL + ' #tutorTabs')
	$('#studentAccordion').load(document.URL + ' #studentAccordion');
}

function update_notify(){
	$('#tutorTabs').load(document.URL + ' #tutorTabs')
	$('#notifications').load(document.URL + ' #notifications')
}

function update_post_view(){
	$('#post-stats').load(document.URL + ' #post-stats');
	$('#comments-div').load(document.URL + ' #comments-div');
}

function queue_formfill(){
	// document.getElementById('studentID').value = cur_student;
	// document.getElementById('class').value = cur_classID;
	document.getElementById('session-student-name').value = $("#upnext").data("wholename");
	document.getElementById('studentID').value = $("#upnext").data("nextstudent");
	var courseSelect = document.getElementById('class');
	for(var i = 0; i < courseSelect.options.length; i++){
		if (courseSelect.options[i].value = $("#upnext").data("nextclass"))
		   courseSelect.selectedIndex = i;
	}
	// document.getElementById('class').selectedIndex = $("#upnext").data("nextclass");
	document.getElementById('session_form').submit();
}