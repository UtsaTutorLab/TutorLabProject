//OPEN AND CLOSE SIDE NAV FUNCTIONS
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
	document.getElementById('nextup').style.fontSize = "14px";
	document.getElementById('next_nextup').style.fontSize = "14px";
    //document.getElementById("main").style.marginLeft = "250px";
    //document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "50px";
    document.getElementById('nextup').style.fontSize = "24px";
	document.getElementById('next_nextup').style.fontSize = "24px";
    //document.getElementById("main").style.marginLeft= "50px";
    //document.body.style.backgroundColor = "white";
}

//LOGIN AJAX
$(function(){
    $('#login-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: $('#login-form').attr('action'), 
            type: 'POST',
            data: $('#login-form').serialize(),
            beforeSend: function(xhr, settings) {
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function(response){
                console.log(response)
                if(response == "false-2"){
                    $("#invalid-login").html("Username or Password is incorrect");
                    $("#invalid-login").fadeIn();
                }else if(response == "false-1"){
                    $("#invalid-login").html("Your account has been deactivated");
                    $("#invalid-login").fadeIn();
                }else{
                    window.location = response;
                }
            }
        });
    });
});

// STUDENT CREATE APPT
$(function(){
    $('#create_appt').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: 'create-appt/', 
            type: 'POST',
            data: $('#create_appt').serialize(),
            success: function(response){
                if(response == "false"){
                    $("#invalid-form").fadeIn();
                } else {
                    $("#invalid-form").hide();
                    $("#success-form").fadeIn();
                }
            }
        });
    });
});

//SHOW STUDENT DELETE EVENT FROM TUTOR CLAENDAR MODAL
function show_delete_event_modal(appt_id){
    $("#eventModalApptID").attr("value", appt_id)
    $("#delete_event_modal").modal("show")
}

// STUDENT DELETE EVENT FROM TUTOR CLAENDAR 
function delete_event(appt_id){
    $("#eventModalApptID").attr("value",function(n, appt_id){
        $.ajax({
            url: 'delete-event/', 
            type: 'POST',
            data: {appt_id: appt_id},
            beforeSend: function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function(response){
                if(response == "true"){
                    update_appt();
                    $("#appt-success-alert").html("Appointment has been deleted");
                    $("#appt-success-alert").fadeIn();
                    setTimeout(function() {
                        $("#appt-alert").fadeOut();
                    }, 5000);
                }else{
                    $("#appt-failed-alert").html("Appointment could not be deleted");
                    $("#appt-failed-alert").fadeIn();
                }
            }
        });
    });
};

// STUDENT DELETE EVENT FROM TUTOR CLAENDAR MODAL
function show_delete_appt_modal(appt_id){
    $("#apptModalApptID").attr("value", appt_id)
    $("#delete_appt_modal").modal("show")
}

// STUDENT DELETE APPT
function delete_appt(){
    $("#apptModalApptID").attr("value",function(n, appt_id){
        $.ajax({
            url: 'delete-appt/', 
            type: 'POST', 
            data: {appt_id: appt_id},
            beforeSend: function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function(response){
                if(response == "true"){
                    update_appt();
                    $("#appt-success-alert").html("Request has been deleted");
                    $("#appt-success-alert").fadeIn();
                    setTimeout(function() {
                        $("#appt-alert").fadeOut();
                    }, 5000);
                }else{
                    $("#appt-failed-alert").html("Request could not be deleted");                
                    $("#appt-failed-alert").fadeIn();
                }
            },
        });
    });
};

// STUDENT CONFIRM NEW TUTOR DATE
function confirm_date(appt_id){
    $.ajax({
        url: 'confirm-appt/',
        type: 'POST', 
        data: {appt_id: appt_id},
        beforeSend: function(xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function(response){
            if(response == "true"){
                update_appt();
                $("#appt-success-alert").html("New appointment time confirmed");
                $("#appt-success-alert").fadeIn();
                setTimeout(function() {
                    $("#appt-alert").fadeOut();
                }, 5000);
            }else{
                $("#appt-failed-alert").html("Could not confirm new appointment time");                
                $("#appt-failed-alert").fadeIn();
            }
        },
    });
};

//STUDENT REQUEST NEW TUTOR
function request_new_tutor(appt_id){
    $.ajax({
        url: 'request-new-tutor/',
        type: 'POST', 
        data: {appt_id: appt_id},
        beforeSend: function(xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function(response){
            if(response == "true"){
                update_appt();
                $("#appt-success-alert").html("New tutor has been requested");
                $("#appt-success-alert").fadeIn();
                setTimeout(function() {
                    $("#appt-alert").fadeOut();
                }, 5000);
            }else{
                $("#appt-failed-alert").html("Could not request new tutor");                
                $("#appt-failed-alert").fadeIn();
            }
        },
    });
}

//RESET ADMIN CREATE TUTOR FORM
$(function() {
    $("#create_tutor").on('hidden.bs.modal', function(){
        $(this).find('form')[0].reset();
        $("#tutor-create-fail-alert").hide();
        $("#tutor-create-success-alert").hide();
    });
})

// TUTOR_ADMIN CREATE NEW TUTOR 
function create_tutor(){
    $('#create_tutor_form').on('submit', function(e){
        e.preventDefault();
        $('#create_tutor_btn').prop('disabled', true).html('loading');
        $.ajax({
            url: 'create-tutor/', 
            type: 'POST',
            data: $('#create_tutor_form').serialize(),
            success: function(response){
                if (response == "false1"){
                    $("#tutor-create-fail-alert").html("User already exists");
                    $("#tutor-create-fail-alert").fadeIn();
                    $('#create_tutor_btn').prop('disabled', false).html('submit');
                }else if(response == "false2"){
                    $("#tutor-create-fail-alert").html("All fields are required");
                    $("#tutor-create-fail-alert").fadeIn();
                    $('#create_tutor_btn').prop('disabled', false).html('submit');
                }else if(response == "false3"){
                    $("#tutor-create-fail-alert").html("Could not create new tutor");
                    $("#tutor-create-fail-alert").fadeIn();
                    $('#create_tutor_btn').prop('disabled', false).html('submit');
                }else if(response == "false4"){
                    $("#tutor-create-fail-alert").html("Could not send email");
                    $("#tutor-create-success-alert").html("New tutor was created");
                    $("#tutor-create-fail-alert").fadeIn();
                    $("#tutor-create-success-alert").fadeIn();
                    $('#tutor-list-panel').load(document.URL + ' #tutor-list-panel')
                    setTimeout(function() {
                        $("#create_tutor").modal('hide');
                    }, 5000);
                } else if(response == "true") {
                    $("#tutor-create-fail-alert").hide();
                    $("#tutor-create-success-alert").html("New tutor was created and activation email sent");
                    $("#tutor-create-success-alert").fadeIn();
                    $('#tutor-list-panel').load(document.URL + ' #tutor-list-panel')
                    setTimeout(function() {
                        $("#create_tutor").modal('hide');
                    }, 5000);
                } else {
                    console.log("invalid request")
                    $("#tutor-create-fail-alert").html("invalid request")
                    $("#tutor-create-fail-alert").fadeIn();
                    $('#create_tutor_btn').prop('disabled', false).html('submit');
                }
            }
        });
    });
}

// ACTIVATE ACCOUNT AND SET PASSWORD
function activate_account(){
    $('#set-password-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: '', 
            type: 'POST',
            data: $('#set-password-form').serialize(),
            beforeSend: function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function(response){
                if (response == "fail1"){
                    $("#password-set-fail-alert").html("Password must be longer than 8 characters");
                    $("#password-set-fail-alert").fadeIn();
                } else if (response == "fail2"){
                    $("#password-set-fail-alert").html("Your passwords do not match");
                    $("#password-set-fail-alert").fadeIn();
                } else {
                    $("#password-set-fail-alert").hide();
                    $("#password-set-success-alert").html("Password Set! Redirecting to your home page...");
                    $("#password-set-success-alert").fadeIn();
                    setTimeout(function() {
                        window.location = response;
                    }, 3000);
                }
            }
        });
    });
}

// CREATE STUDENT AJAX
$(function(){
    $('#create-student-form').on('submit', function(e){
        e.preventDefault();
        $('#create-student-btn').prop('disabled', true).html('loading');
        $.ajax({
            url: '', 
            type: 'POST',
            data: $('#create-student-form').serialize(),
            beforeSend: function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function(response){
                if (response == "false1"){
                    $("#create-student-fail-alert").html("Student already exists, if you feel this is incorrect please email us.");
                    $("#create-student-fail-alert").fadeIn();
                    $('#create-student-btn').prop('disabled', false).html('submit');
                }else if(response == "false2"){
                    $("#create-student-fail-alert").html("All fields are required");
                    $("#create-student-fail-alert").fadeIn();
                    $('#create-student-btn').prop('disabled', false).html('submit');
                }else if(response == "false3"){
                    $("#create-student-fail-alert").html("Could not create Student");
                    $("#create-student-fail-alert").fadeIn();
                    $('#create-student-btn').prop('disabled', false).html('submit');
                }else if(response == "false4"){
                    $("#create-student-fail-alert").html("Could not create account. Please check the abc123 you entered");
                    $("#create-student-fail-alert").fadeIn();
                    $('#create-student-btn').prop('disabled', false).html('submit');
                } else if(response == "true") {
                    $("#create-student-fail-alert").hide();
                    $("#create-student-success-alert").html("Account was created and an activation link was sent to your @my.utsa.edu email");
                    $("#create-student-success-alert").fadeIn();
                } else {
                    console.log("invalid request")
                    $("#create-student-fail-alert").html("invalid request")
                    $("#create-student-fail-alert").fadeIn();
                    $('#create-student-btn').prop('disabled', false).html('submit');
                }
            }
        });
    });
});

// TUTOR VIEWED NOTIFICATIONS
function viewed(tutor_id){
    $.ajax({
            url: 'viewed/', 
            type: 'POST',
            data: {'tutor_id': tutor_id},
            beforeSend: function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function(response){
                console.log(response)
                if(response == 'true'){
                    $('#notification_num').hide()
                }
            }
    });
}

// DELETE TUTOR NOTIFICATION
function delete_notification(note_id){
    $.ajax({
            url: 'delete-notification/', 
            type: 'POST',
            data: {'note_id': note_id},
            beforeSend: function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function(response){
                console.log(response)
                if(response == 'true'){
                    $('#notify'+note_id).hide()
                    $("#success-alert").html("Notification deleted");
                    $("#success-alert").fadeIn();
                    setTimeout(function() {
                        $("#success-alert").hide();
                    }, 3000);
                }else{
                    $("#invalid-alert").html("Notification could not be deleted");
                    $("#invalid-alert").fadeIn();
                    setTimeout(function() {
                        $("#invalid-alert").hide();
                    }, 3000);
                }
            }
    });
}

// TUTOR ADMIN SEND NOTIFICATION
$(function(){
    $('#send_notification_form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: 'send-notification/', 
            type: 'POST',
            data: $('#send_notification_form').serialize(),
            success: function(response){
                console.log(response)
                if(response == 'true'){
                    $("#success-notification-alert").html("Notification was sent")
                    $("#success-notification-alert").fadeIn()
                    $('#msg-submit-btn').prop('disabled', true).html("Sending")
                    setTimeout(function() {
                        $("#create_notification").modal('hide');
                        $("#success-notification-alert").hide()
                        $('#msg-submit-btn').prop('disabled', false).html("Submit")
                        $("#create_notification").on('hidden.bs.modal', function(){
                            $(this).find('form')[0].reset();
                        });
                    }, 3000);
                }else if(response == "false1"){
                    $("#invalid-notification-alert").html("Not all notifications could not be sent")
                    $("#indalid-notification-alert").fadeIn()
                }
            }
        });
    });
});

// TUTOR ADMIN EDIT SUREVY QUESTIONS
function update_questions(){
    // var i;
    var questions = [];
    for(i = 0; i<5; i++){
        var q = [];
        q.push($("#question_id"+(i+1)).val());
        q.push($("#question"+(i+1)).val());
        q.push($("#question_"+(i+1)+"_div").find(":selected").val());
        questions.push(q);
    }
    $.ajax({
            url: 'edit-questions/', 
            type: 'POST',
            data: {'questions[]': questions},
            success: function(response){
                if(response == "true"){
                    $("#edit-questions-success-alert").html("Questions have been updated")
                    $("#edit-questions-success-alert").fadeIn()
                    setTimeout(function() {
                        $("#edit_survey_questions").modal('hide');
                        $("#edit-questions-success-alert").hide();
                    }, 3000);
                }else{
                    $("#edit-questions-failed-alert").html("Questions could not be updated")
                    $("#edit-questions-failed-alert").fadeIn()
                    setTimeout(function() {
                        $("#edit_survey_questions").modal('hide');
                        $("#edit-questions-failed-alert").hide();
                    }, 3000);
                }
            }
        });
}

//TUTOR ADMIN SHOW RANGE VALUE
function toggle_range_questions(){
    $("#edit_survey_questions").modal('toggle');
    $("#edit_range_value").modal('toggle');
    setTimeout(function() {
        $("body").addClass("modal-open");
    }, 500);
}

// TUTOR ADMIN ADD RANGE VALUE
function add_range_value(){
    var lowValue = $("#low_value").val();
    var highValue = $("#high_value").val();
    var test = true;
    if(lowValue == ""){
        $("#low_div").removeClass("form-group has-error");
        $("#inputError1").remove();
        test = false;
        $("#low_div").addClass("form-group has-error");
        $("#low_div").append('<label class="control-label" id="inputError1">Input can not be blank</label>')
    }else{
        $("#low_div").removeClass("form-group has-error");
        $("#inputError1").remove();
    }
    if(highValue == ""){
        $("#high_div").removeClass("form-group has-error");
        $("#inputError2").remove();
        test = false;
        $("#high_div").addClass("form-group has-error");
        $("#high_div").append('<label class="control-label" id="inputError2">Input can not be blank</label>')
    }else{
        $("#high_div").removeClass("form-group has-error");
        $("#inputError2").remove();
    }
    if(test == true){
        $.ajax({
            url: 'add-range-value/',
            type: 'POST', 
            data: {lowValue: lowValue, highValue:highValue},
            beforeSend: function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function(response){
                if(response['bool'] == "true"){
                    $("#low_value").val("");
                    $("#high_value").val("");
                    $("#my-range-value-list-group").append('<a class="list-group-item" id="choice_list'+response['id']+'">'
                        +lowValue+" to "+highValue+ 
                        '<span class="close" onclick="delete_range_value('+response['id']+')" style="margin-top: -3px">x</span></a>'
                    );
                    $('#questions_div').load(document.URL + ' #questions_div')
                }else{
                    $("#edit-value-range-failed-alert").html("Range value could not be added")
                    $("#edit-value-range-failed-alert").fadeIn()
                    setTimeout(function() {
                        $("#edit-value-range-failed-alert").fadeOut()
                    },3000);
                }
            },
        });
    }
}

// TUTOR ADMIN DELETE RANGE VALUE
function delete_range_value(id){
    $.ajax({
        url: 'delete-range-value/',
        type: 'POST', 
        data: {id: id},
        beforeSend: function(xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function(response){
            if(response['bool']=="true"){
                $("#choice_list"+id).remove();
                $('#questions_div').load(document.URL + ' #questions_div')
            }else{
                $("#edit-value-range-failed-alert").html("Range value could not be deleted")
                $("#edit-value-range-failed-alert").fadeIn()
                setTimeout(function() {
                    $("#edit-value-range-failed-alert").fadeOut()
                },3000);
            }
        }
    });
}

// NEW TERM ADDED
$(function() {
    $('#add_term_form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: 'add-term/',
            type: 'POST',
            data: $('#add_term_form').serialize(),
            success: function(response){
                console.log(response)
                if(response == "true"){
                    $("#delete-term-div").load(document.URL + " #delete-term-list")
                    $("#edit-term-div").load(document.URL + " #edit-term-list")
                    $("#add-term-success-alert").html("Term successfully added")
                    $("#add-term-success-alert").fadeIn();
                    setTimeout(function() {
                        $("#add-term-success-alert").fadeOut();
                    }, 1500);
                } else if (response == "duplicate"){
                    $("#add-term-failed-alert").html("Already term with same name")
                    $("#add-term-failed-alert").fadeIn()
                    setTimeout(function() {
                        $("#add-term-failed-alert").fadeOut();
                    }, 3000);
                } else {
                    $("#add-term-failed-alert").html("Failed to add term")
                    $("#add-term-failed-alert").fadeIn()
                    setTimeout(function() {
                        $("#add-term-failed-alert").fadeOut();
                    }, 3000);
                }
            },
        });
    });
});

// DELETE TERM
$(function() {
    $('#delete_term_form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: 'delete-term/',
            type: 'POST',
            data: $('#delete_term_form').serialize(),
            success: function(response){
                console.log(response)
                if(response == "true"){
                    $("#delete-term-div").load(document.URL + " #delete-term-list")
                    $("#edit-term-div").load(document.URL + " #edit-term-list")
                    $("#delete-term-success-alert").html("Term successfully deleted")
                    $("#delete-term-success-alert").fadeIn()
                    setTimeout(function() {
                        $("#delete-term-success-alert").fadeOut();
                    }, 1500);
                } else if (response == "doesnotexist"){
                    $("#delete-term-failed-alert").html("Term does not exist")
                    $("#delete-term-failed-alert").fadeIn()
                    setTimeout(function() {
                        $("#delete-term-failed-alert").fadeOut();
                    }, 3000);
                } else {
                    $("#delete-term-failed-alert").html("Failed to delete term")
                    $("#delete-term-failed-alert").fadeIn()
                    setTimeout(function() {
                        $("#delete-term-failed-alert").fadeOut();
                    }, 3000);
                }
            },
        });
    });
});

// EDIT TERM
$(function() {
    $('#edit_term_form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: 'edit-term/',
            type: 'POST',
            data: $('#edit_term_form').serialize(),
            success: function(response){
                console.log(response)
                if(response == "true"){
                    $("#edit-term-div").load(document.URL + " #edit-term-list")
                    $("#edit-term-success-alert").html("Term successfully updated")
                    $("#edit-term-success-alert").fadeIn()
                    setTimeout(function() {
                        $("#edit-term-success-alert").fadeOut();
                    }, 3000);
                } else if (response == "doesnotexist"){
                    $("#edit-term-failed-alert").html("Already term with same name")
                    $("#edit-term-failed-alert").fadeIn()
                    setTimeout(function() {
                        $("#edit-term-failed-alert").fadeOut();
                    }, 3000);
                } else {
                    $("#edit-term-failed-alert").html("Failed to add term")
                    $("#edit-term-failed-alert").fadeIn()
                    setTimeout(function() {
                        $("#edit-term-failed-alert").fadeOut();
                    }, 3000);
                }
            },
        });
    });
});

// POPULATE SELECTED TERMS START/END DATES
$(document).on('change', '#edit-term-list', function() {
    var element = document.getElementById("edit-term-list");

    $('edit_start_date').attr("placeholder"," ");
    // $('#edit_start_date').val(element.options[element.selectedIndex].dataset.start);
    $('#edit_start').datepicker("setDate", element.options[element.selectedIndex].dataset.start);
    
    $('edit_end_date').attr("placeholder"," ");
    // $('#edit_end_date').val(element.options[element.selectedIndex].dataset.end);
    $('#edit_end').datepicker("setDate", element.options[element.selectedIndex].dataset.end);
});

// TUTOR ADMIN ISSUE LIST UPDATES
function add_issue(){
    var inputValue = document.getElementById("issue_input").value;
    $.ajax({
        url: 'add-issue-list/',
        type: 'POST', 
        data: {issue: inputValue},
        beforeSend: function(xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function(response){
            if(response["bool"] == "true"){
                update_tutor_admin_view();                
                $("#edit-issue-list-success-alert").html("Added issue to list")
                $("#edit-issue-list-success-alert").fadeIn()
                setTimeout(function() {
                    $("#edit-issue-list-success-alert").fadeOut()
                }, 3000);
            }else if(response == "false1"){
                $("#edit-issue-list-failed-alert").html("Plese enter an issue")
                $("#edit-issue-list-failed-alert").fadeIn()
                setTimeout(function() {
                    $("#edit-issue-list-failed-alert").fadeOut()
                }, 3000);
            }else if(response == "false2"){
                $("#edit-issue-list-failed-alert").html("Could not create issue item")
                $("#edit-issue-list-failed-alert").fadeIn()
                setTimeout(function() {
                    $("#edit-issue-list-failed-alert").fadeOut()
                }, 3000);
            }else{
                $("#edit-issue-list-failed-alert").html("Failed to add issue")
                $("#edit-issue-list-failed-alert").fadeIn()
                setTimeout(function() {
                    $("#edit-issue-list-failed-alert").fadeOut()
                }, 3000);
            }
        },
    });
}

function delete_issue(id){
    $.ajax({
        url: 'delete-issue-list/',
        type: 'POST', 
        data: {issue_id: id},
        beforeSend: function(xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function(response){
            if(response == "true"){
                update_tutor_admin_view();      
                $("#edit-issue-list-success-alert").html("Issue deleted")
                $("#edit-issue-list-success-alert").fadeIn()
                setTimeout(function() {
                    $("#edit-issue-list-success-alert").fadeOut()
                }, 3000);
            }else{
                $("#edit-issue-list-failed-alert").html("Failed to delete issue")
                $("#edit-issue-list-failed-alert").fadeIn()
                setTimeout(function() {
                    $("#edit-issue-list-failed-alert").fadeOut()
                }, 3000);
            }
        },
    });
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