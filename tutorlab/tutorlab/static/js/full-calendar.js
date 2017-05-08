// fullCalendar Script
$(document).ready(function() {
    $.ajax({
        url : "get-events/", // the endpoint
        type : "GET", // http method
        async: false,
        success: function(s){
            console.log(s)
            appt_events = s;
        }
    });

    $('#calendar').fullCalendar({
        header: {
            left: "prev,today,next",
            center: "title",
            right: " "
        },
        slotDuration: "00:15:00",
        // editable: 'False',
        events: appt_events, //parse out the json array "events"
        eventClick: function(event, jsEvent, view) {
            $('#modalabc123').html(event.title);
            $('#student').attr('value', event.title);
            $('#modalStudent').attr('value', event.student).html(event.student);
            $('#modalDate').html(moment(event.start).format('MMM DD, YYYY h:mm a'));
            $('#modalCourse').html(event.course);
            $('#classID').attr('value', event.course);
            $('#modalDescription').html(event.description);
            $('#modalID').attr('value', event.id);
            if(event.confirmed){
                $('#modalConfirmed').html("Student has confirmed this appointment");
            } else {
                $('#modalConfirmed').html("Student has not confirmed this appointment yet");
                $('#start-session-btn').prop('disabled', true);
                $('#change-date-btn').prop('disabled', true);
            }
            $('#calendarModal').modal('show');
        }
    });//end fullCalendar
    
    $('#appt_schedule').click(function() {
        window.setTimeout(clickToday, 200);
    });

    function clickToday() {
        $('.fc-today-button').click();
    }
});//end doc ready

//START APPOINTMENT SESSION
function start_session(){
     $.ajax({
            url: 'start-session/', 
            type: 'POST', 
            data: $('#send_date').serialize(),
     });
     delete_event();
}

//ADD REQUEST TO CALENDAR
function add_event(appt_pk){
    console.log(appt_pk)
      $.ajax({
        url : "add-event/", 
        type : "POST", 
        data : {appt_pk: appt_pk},
        beforeSend: function(xhr, settings) {
            console.log("Before Send");
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function(response){
            console.log(response)
            $('#calendar').fullCalendar('removeEvents');
            getFreshEvents();
            // update_appt();
        },
    });
}

//DELETES EVENT FROM CALENDAR
function delete_event(){
    $("#modalID").attr("value",function(n, id){
        $.ajax({
            url : "delete-event/",
            type: "POST",
            data: {deleted_appt : id},
            beforeSend: function(xhr, settings) {
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function(response){
                console.log(response)
                $('#calendar').fullCalendar('removeEvents', id);
            }
        });
    });
}
        
//SHOW CHANGE DATE MODAL
function change_date(){
    var date = $("#modalDate").text()
    $("#modalID").attr("value", function(x, id){
        $('#event_ID').attr("value", id)
        $('#modalOldDate').html(date);
        $('#request_new_date').modal('show');
    });
};

//CHANGE DATE OF APPOINTMENT
$(function(){
    $('#send_date').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: 'send-date/',
            type: 'POST',
            data: $('#send_date').serialize(),
            success: function(response){
                if(response == "false"){
                    $("#appt-send-failed-alert").fadeIn();
                }else{
                    console.log(response)
                    $("#appt-send-failed-alert").hide();
                    $("#appt-send-success-alert").fadeIn();
                    $('#calendar').fullCalendar('removeEvents');
                    getFreshEvents();
                    setTimeout(function() {
                        $('#request_new_date').modal('hide');
                    }, 5000);
                }
            }
        });
    });
});

//GETS ALL CALENDAR EVENTS
function getFreshEvents(){
    console.log('getting fresh events')
    $.ajax({
        url : "get-events/", // the endpoint
        type : "GET", // http method
        async: false,
        success: function(s){
                console.log(s)
	        	freshevents = s;
	        }
    });
    $('#calendar').fullCalendar('addEventSource', freshevents);
}

// NEEDED FOR AJAX CSRFToken
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// NEEDED FOR AJAX CSRFToken
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});