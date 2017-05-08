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

$(document).ready(function() {
    //for question sets
    $("#add-to-set-btn").prop('disabled', true);
    $("#custom-issue-btn").prop('disabled', true);

    // CLASS ISSUE SET
    $("#class-list").change(function () {
        $("#add-to-set-btn").prop('disabled', false);
        $("#custom-issue-btn").prop('disabled', false);
        var className = $(this).find("option:selected").text();
        var courseId = $("#class-list").val();
        // var listIndex = $(this).find("option:selected").index();
        $.ajax({
            url: '../instructor/get-custom-issue-list/',
            type: 'GET',
            dataType: 'json',
            data: {'course_id':courseId},
            success: function(response){
                if(response['bool'] == "true"){
                    update_list(className, response['issueList'], response['selectList'])
                }else{
                    //error message
                }
            }
        });
    });

    //for importing students
    $("#xls-input-file").prop("disabled", true);
    $("#submit-file-btn").prop("disabled", true);

    // ADD STUDENT CLASS SET
     $("#import-student-class-list").change(function () {
        $("#xls-input-file").prop('disabled', false);
        $("#import-file-btn").removeClass('disabled');
     });
});

function show_custom(){
    $("#custom-issue-div").show();
    $("#common-issue-div").hide();
}

function show_list(){
    $("#custom-issue-div").hide();
    $("#common-issue-div").show();
}

/**
 * Ajax call to add issue(s) to the set for the selected class
 */
function add_to_set(){
    var selectList = document.getElementById("issue-list-select");
    var classId = $("#class-list").val();
    var classIndex = $("#class-list").find("option:selected").index();
    var className = $(this).find("option:selected").text();
    var selectedIssues = [];
    for (var i = 0; i < selectList.length; i++) {
        if (selectList.options[i].selected) selectedIssues.push(selectList.options[i].value);
    }
    if(selectedIssues.length == 0){
        $("#custom-issue-failed-alert").html("No issues selected!").fadeIn();
        setTimeout(function() {
            $("#custom-issue-failed-alert").fadeOut()
        }, 5000);
    }else{
        $.ajax({
            url: '../instructor/add-custom-issue-list/',
            type: 'POST',
            dataType: 'json',
            data: {'course_id':classId, 'issue_list[]':selectedIssues},
            success: function(response){
                if(response['bool'] == "true"){
                    update_list(className, response['newIssueList'], response['selectList']);
                }else{
                    //error
                }
            }
        });
    }
}

/**
 * 
 * @param {*} issueId 
 */
function delete_from_set(issueId){
    var classId = $("#class-list").val();
    var className = $(this).find("option:selected").text();
    $.ajax({
        url: '../instructor/delete-issue-from-set/',
        type: 'POST',
        dataType: 'json',
        data: {'issue_id':issueId, 'class_id':classId},
        success: function(response){
            if(response['bool'] == "true"){
                update_list(className, response['issueList'], response['selectList']);
            }else{
                //error
                console.log(response)
            }
        }
    });
}

/**
 * Updates the "my-issue-list-group" div
 * 
 * @param {*} className 
 * @param {*} issueList 
 */
function update_list(className, issueList, selectList){
    //update issue select list
    $("#issue-list-select").empty();
    if(selectList.length > 0){
        for(x = 0; x < selectList.length; x++){
            $("#issue-list-select").append('<option value='+selectList[x]['id']+'>'+selectList[x]['issue']+'</option>');
        }
    }
    //update issue set list
    $("#my-issue-list-group").empty();
    $("#class-name").html("List of questions for " + className);
    if(issueList.length > 0){
        for(x = 0; x < issueList.length; x++ ){
            $("#my-issue-list-group").append('<a class="list-group-item">'
                +issueList[x][1]+ 
                '<span class="close" onclick="delete_from_set('+issueList[x][0]+')" style="margin-top: -3px">x</span></a>'
                );
        }
    }else{
        $("#my-issue-list-group").prepend('<h5>No issue set created</h5>');
    }
    
}

/**
 * 
 * @param {String} course 
 * @param {int} course_id 
 */
function get_students(course, course_id, course_num){
    $("#student-title").html("Students in " + course);
    $("#student-list-ul").empty();
    $.ajax({
        url: '../instructor/get-students/',
        type: 'GET',
        data: {'course_id':course_id},
        success: function(response){
            if(response['bool'] == "true"){
                if(response['student_list'].length > 0){
                    for(x = 0; x < response['student_list'].length; x++ ){
                        $("#student-list-ul").prepend("<a href='./"+ response['student_list'][x][2] +"/"+ course_num +"'>"+response['student_list'][x][0]+ " " + response['student_list'][x][1] + "</a><br>");
                    }
                }else{
                    $("#student-list-ul").prepend("<h5>No Students added to this class</h5>");
                }
            }
        }
    });
}

// FILE UPLOAD SCRIPT IN ADD STUDENT MODAL
$(function() {
  // We can attach the `fileselect` event to all file inputs on the page
  $(document).on('change', ':file', function() {
    var input = $(this),
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [label]);
  });

  // We can watch for our custom `fileselect` event like this
  $(document).ready( function() {
      $(':file').on('fileselect', function(event, label) {
          var input = $(this).parents('.input-group').find(':text');
          if( input.length ) {
              input.val(label);
          }
          if(input.val().match(/.xls$/) != null){
            $("#submit-file-btn").prop('disabled', false);
          }else{
            $("#submit-file-btn").prop('disabled', true);
          }
      });
  });
});

// UPLOAD XLS FILE 
function upload_file(){
        var val = $("#import-student-class-list").val();
        var className = $("#import-student-class-list").find("option:selected").text();
        var file = $('#xls-input-file').get(0).files[0];
        var formdata = new FormData();
        formdata.append('file', file);
        formdata.append('course_id', val);
        $.ajax({
            url: '../instructor/add-students-to-class/',
            type: 'POST',
            processData: false,
            contentType: false,
            data: formdata,
            success: function(response){
                if(response['bool'] == "true"){
                    $("#add-student-to-class-failed-alert").fadeOut();
                    $("#xls-input-file").val("");
                    $("#xls-input-file-text").val("");
                    $("#submit-file-btn").prop('disabled', true);
                    if(response['new_count'] > 0){
                        $("#add-student-to-class-success-alert").html(response['new_count'] +" Students added to " + className).fadeIn();
                    }else{
                        $("#add-student-to-class-success-alert").html("No new students added to " + className).fadeIn();
                    }
                    setTimeout(function(){
                        $("#add-student-to-class-success-alert").fadeOut();
                    },5000);
                }
                if(response['bool'] == "false"){
                    $("#add-student-to-class-failed-alert").html(response['msg']).fadeIn();
                }
            }
        });
}
