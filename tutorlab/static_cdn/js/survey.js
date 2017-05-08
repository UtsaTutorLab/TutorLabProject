// TRACKS SCORE, CLICKS, AND PROGRESS BAR
function count_score(score){
  var int_score = parseInt(score);
  var score_count = parseInt($("#score_count").val());
  var click_count = $("#click_count").val();
  var bar_value = parseInt($("#progress_bar").val());
  var old_count = click_count;
  score_count+=int_score;
  click_count++;
  bar_value+=20;
  id_show = "#question" + click_count;
  id_hide = "#question" + old_count; 
  $(id_hide).hide();
  $(id_show).fadeIn();
  $("#answer"+old_count).val(int_score)
  $("#click_count").val(click_count);
  $("#score_count").val(score_count);
  $("#progress_bar").val(bar_value)
  $("#progress-bar").html(bar_value+"%");
  document.getElementById("progress-bar").style["width"] = bar_value+"%";
}

// SUBMIT SURVEY
$(function() {
    $('#survey-submit-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: '', 
            type: 'POST',
            data: $('#survey-submit-form').serialize(),
            success: function(response){
              console.log(response)
              if(response == "fail1"){
                $("#invalid-form").html("Your form is invalid");
                $("#invalid-form").fadeIn();
              }else{
                console.log(response)
                window.location = response;
              }
            }
        });
    });
});