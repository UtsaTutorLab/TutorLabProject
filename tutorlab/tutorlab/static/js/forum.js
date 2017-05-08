// CREATE POST AJAX FORM
function create_post(){
    $('#create-new-post-form').on('submit', function(e){
        e.preventDefault();
        var x = document.forms["create-new-post-form"]["post_title"].value;
        var y = document.forms["create-new-post-form"]["post_course"].value;
        var z = document.forms["create-new-post-form"]["post_content"].value;
        if( x == null || x == "" ){
            $('#create-post-failed-alert').html('Title is required');
            $('#create-post-failed-alert').fadeIn();
        }else if( y == null || y == ""){
            $('#create-post-failed-alert').html('Course number is required');
            $('#create-post-failed-alert').fadeIn();
        }else if( z == null || z == ""){
            $('#create-post-failed-alert').html('Message is required');
            $('#create-post-failed-alert').fadeIn();
        }else{
            $.ajax({
                url: 'ajax-create-post/', 
                type: 'POST',
                data: $('#create-new-post-form').serialize(),
                success: function(response){
                    console.log(response)
                    if(response == "true"){
                        $('#create-post-failed-alert').hide();
                        $('#create-post-success-alert').html('Post Created');
                        $('#create-post-success-alert').fadeIn();
                        $('#your-post-list').load(document.URL + ' #your-post-list');
                        setTimeout(function() {
                            $("#create-post").modal('hide');
                            $("#create-post-success-alert").hide();
                        }, 3000);
                    }else{
                        $('#create-post-failed-alert').html('Could not create post');
                        $('#create-post-failed-alert').fadeIn();
                    }
                }
            });
        }
    });
}

// AJAX INCREASE VIEW COUNT ON CLICK 
function increase_view_count(id){
    console.log("view clicked");
    $.ajax({
        url: 'ajax-increase-view-count/', 
        type: 'POST',
        data: {'id':id},
        success: function(response){
            console.log(response)
        }
    });
}

// CREATE COMMENT AJAX FORM
$(function(){
    $('#create-new-comment-form').on('submit', function(e){
        e.preventDefault();
        var $form = $(this);
        $.ajax({
            url: 'ajax-create-comment/', 
            type: 'POST',
            data: $('#create-new-comment-form').serialize(),
            success: function(response){
                console.log(response)
                if(response == "true"){
                    $('#create-comment-failed-alert').hide();
                    $('#create-comment-success-alert').html('Comment Posted');
                    $('#create-new-comment-form-div').hide();
                    $('#create-comment-success-alert').fadeIn();
                    update_post_view()
                    $('#comment_message').css("height", "33");
                    $('#create-new-comment-form-div').css("margin-bottom", "0px");
                    $('#comment-submit-btn').hide()
                    setTimeout(function() {
                        $form.get(0).reset();
                        $("#create-comment-success-alert").hide();
                        $('#create-new-comment-form-div').fadeIn();
                    }, 3000);
                }else if(response == "false1"){
                    console.log(response)
                    $('#create-comment-failed-alert').html('Could not post comment: You have to write a message');
                    $('#create-comment-failed-alert').fadeIn();
                    setTimeout(function() {
                        $("#create-comment-failed-alert").hide();
                    }, 3000);
                }else{
                    console.log(response)
                    $('#create-comment-failed-alert').html('Unexpected error');
                    $('#create-comment-failed-alert').fadeIn();
                    setTimeout(function() {
                        $("#create-comment-failed-alert").hide();
                    }, 3000);
                }
            }
        });
    });
});

// BOOKMARK BUTTON AJAX
function bookmark(post_id){
    var x = document.getElementById("bookmark_btn").value;
    console.log(post_id)
    if(x == 0){
        $('.glyphicon-bookmark').css("color","rgb(204, 11, 4)");
        document.getElementById("bookmark_btn").value = 1;
    }else {
        $('.glyphicon-bookmark').css("color","rgb(51, 51, 51)");
        document.getElementById("bookmark_btn").value = 0;
    }
    $.ajax({
        url: 'ajax-bookmark-post/', 
        type: 'POST',
        data: {'post_id':post_id},
        success: function(response){
            console.log(response);
            if(response == "false"){
                $('.glyphicon-bookmark').css("color","rgb(51, 51, 51)")
                document.getElementById("bookmark_btn").value = 0;
            }
        }
    });
}

// UP LIKE POST BUTTON AJAX
function uplikepost(val, post_id){
    var up = $("#like-button-up").val();
    var down = $("#like-button-down").val();
    var vote_num = parseInt($("#vote-value").attr('value'));
    if(up == 0){
        $('#like-button-up').css("color","rgb(204, 11, 4)");
        $("#like-button-up").val(1);
        if(down != 0){
            $('#like-button-down').css("color","rgb(51, 51, 51)");
            $("#like-button-down").val(0);
            vote_num+=2
            $('#vote-value').html(vote_num);
            $("#vote-value").attr('value',vote_num);
        }else{
            vote_num+=1
            $('#vote-value').html(vote_num);
            $("#vote-value").attr('value',vote_num);
        }
    }else{
        $('#like-button-up').css("color","rgb(51, 51, 51)");
        $("#like-button-up").val(0);
        vote_num-=1
        $('#vote-value').html(vote_num);
        $("#vote-value").attr('value', vote_num);
    }
    $.ajax({
        url: 'ajax-vote-post/', 
        type: 'POST',
        data: {'value': val, 'post_id':post_id},
        success: function(response){
            console.log(response);
            if(response == 'invalid'){
                console.log("could not place vote")
            }
        }
    });
}

// DOWN LIKE BUTTON AJAX
function downlikepost(val, post_id){
    var up = $("#like-button-up").val();
    var down = $("#like-button-down").val();
    var vote_num = parseInt($("#vote-value").attr('value'));
    if(down == 0){
        $('#like-button-down').css("color","rgb(204, 11, 4)");
        $("#like-button-down").val(1);
        if(up == 1){
            $('#like-button-up').css("color","rgb(51, 51, 51)");
            $("#like-button-up").val(0);
            vote_num-=2
            $('#vote-value').html(vote_num);
            $("#vote-value").attr('value', vote_num);
        }else{
            vote_num-=1
            $('#vote-value').html(vote_num);
            $("#vote-value").attr('value', vote_num);
        }
    }else{
        $('#like-button-down').css("color","rgb(51, 51, 51)");
        $("#like-button-down").val(0);
        vote_num+=1
        $('#vote-value').html(vote_num);
        $("#vote-value").attr('value', vote_num);
    }
    $.ajax({
        url: 'ajax-vote-post/', 
        type: 'POST',
        data: {'value': val, 'post_id':post_id},
        success: function(response){
            console.log(response);
            if(response == 'invalid'){
                console.log("could not place vote")
            }
        }
    });
}

// FLAG POST AJAX
function postflag(post_id){
    var x = document.getElementById("flag_btn").value;
    console.log(post_id)
    if(x == 0){
        $('.glyphicon-flag').css("color","rgb(204, 11, 4)");
        document.getElementById("flag_btn").value = 1;
    }else {
        $('.glyphicon-flag').css("color","rgb(51, 51, 51)");
        document.getElementById("flag_btn").value = 0;
    }
     $.ajax({
        url: 'ajax-flag-post/', 
        type: 'POST',
        data: {'post_id':post_id},
        success: function(response){
            console.log(response);
            if(response == "false"){
                $('.glyphicon-flag').css("color","rgb(51, 51, 51)")
                document.getElementById("flag").value = 0;
            }
        }
    });
}


// COMMENT TEXTAREA ANIMATION
$(function(){
    $('#comment_message').focus (function() {
        $('#comment_message').animate({
            height: 200
        }, 500);
        $('#create-new-comment-form-div').animate({
            marginBottom: 55
        }, 500);
        $('#comment-submit-btn').fadeIn();
    });
})

// UP LIKE COMMENT AJAX
function uplikecomment(val, comment_id){
    var up = $("#like-button-up-"+comment_id).val();
    var down = $("#like-button-down-"+comment_id).val();
    var vote_num = parseInt($("#vote-value-"+comment_id).attr('value'));
    if(up == 0){
        $('#like-button-up-'+comment_id).css("color","rgb(204, 11, 4)");
        $('#like-button-up-'+comment_id).val(1);
        if(down != 0){
            $('#like-button-down-'+comment_id).css("color","rgb(51, 51, 51)");
            $('#like-button-down-'+comment_id).val(0);
            vote_num+=2
            $('#vote-value-'+comment_id).html(vote_num);
            $('#vote-value-'+comment_id).attr('value',vote_num);
        }else{
            vote_num+=1
            $('#vote-value-'+comment_id).html(vote_num);
            $('#vote-value-'+comment_id).attr('value',vote_num);
        }
    }else{
        $('#like-button-up-'+comment_id).css("color","rgb(51, 51, 51)");
        $('#like-button-up-'+comment_id).val(0);
        vote_num-=1
        $('#vote-value-'+comment_id).html(vote_num);
        $('#vote-value-'+comment_id).attr('value', vote_num);
    }
    $.ajax({
        url: 'ajax-vote-comment/', 
        type: 'POST',
        data: {'value': val, 'comment_id':comment_id},
        success: function(response){
            console.log(response);
            if(response == 'invalid'){
                console.log("could not place vote")
            }
        }
    });
}

// DOWN LIKE COMMENT AJAX
function downlikecomment(val, comment_id){
    var up = $('#like-button-up-'+comment_id).val();
    var down = $('#like-button-down-'+comment_id).val();
    var vote_num = parseInt($("#vote-value-"+comment_id).attr('value'));
    if(down == 0){
        $('#like-button-down-'+comment_id).css("color","rgb(204, 11, 4)");
        $('#like-button-down-'+comment_id).val(1);
        if(up == 1){
            $('#like-button-up-'+comment_id).css("color","rgb(51, 51, 51)");
            $('#like-button-up-'+comment_id).val(0);
            vote_num-=2
            $('#vote-value-'+comment_id).html(vote_num);
            $('#vote-value-'+comment_id).attr('value', vote_num);
        }else{
            vote_num-=1
            $('#vote-value-'+comment_id).html(vote_num);
            $("#vote-value-"+comment_id).attr('value', vote_num);
        }
    }else{
        $('#like-button-down-'+comment_id).css("color","rgb(51, 51, 51)");
        $('#like-button-down-'+comment_id).val(0);
        vote_num+=1
        $('#vote-value-'+comment_id).html(vote_num);
        $('#vote-value-'+comment_id).attr('value', vote_num);
    }
    $.ajax({
        url: 'ajax-vote-comment/', 
        type: 'POST',
        data: {'value': val, 'comment_id':comment_id},
        success: function(response){
            console.log(response);
            if(response == 'invalid'){
                console.log("could not place vote")
            }
        }
    });
}

// SEARCH FORUM AJAX
$(function() {
    $('#forum-search').keyup(function() {
        $.ajax({
            type: "GET",
            url: "ajax-forum-search/",
            data: {
                'search_text' : $('#forum-search').val(),
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR){
    $('#search-results').html(data)
}

// ALLOW TAB IN TEXT AREA
$(function(){
    $("textarea").keydown(function(e) {
        if(e.keyCode === 9) { // tab was pressed
            // get caret position/selection
            var start = this.selectionStart;
            var end = this.selectionEnd;

            var $this = $(this);
            var value = $this.val();

            // set textarea value to: text before caret + tab + text after caret
            $this.val(value.substring(0, start)
                        + "\t"
                        + value.substring(end));

            // put caret at right position again (add one for the tab)
            this.selectionStart = this.selectionEnd = start + 1;

            // prevent the focus lose
            e.preventDefault();
        }
    });
});