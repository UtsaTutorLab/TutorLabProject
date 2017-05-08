from django.conf import settings
from django.core import signing
from django.core.urlresolvers import reverse
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Survey, Question
from ta_tutor.models import Tutor
import decimal, json, sys
    
# SAVES SURVEY INFO
def survey(request, token):
    try:
        survey_id = signing.loads(token,
                            max_age = (3600 * 24) * 2, # expires in 2 days
                            salt=settings.SECRET_KEY)
    except signing.BadSignature:
        return HttpResponse(
                json.dumps("survey/survey-404/too_long"),
                content_type="application/json"
            )
    if request.method == 'POST':
        try: 
            survey = Survey.objects.get(id=survey_id)
        except:
            return HttpResponse(
                json.dumps("survey/survey-404/no_survey"),
                content_type="application/json"
            )
        if survey.token != token:
            return HttpResponse(
                json.dumps("survey/survey-404/already_used"),
                content_type="application/json"
            )

        click_count = request.POST.get('click_count')
        score_count = request.POST.get('score_count')
        
        answer = []
        for x in range(0,5):
            ans = request.POST.get('answer'+str(x+1))
            answer.append(ans)

        comment = request.POST.get('comment')

        if int(click_count) > 6 or int(score_count) > 25:
            return HttpResponse(
                json.dumps("fail1"),
                content_type="application/json"
            )
        else:
            question_set = Question.objects.all()
            survey = Survey.objects.get(id=survey_id)
            survey.ans1 = question_set[0].question_text + " = " + answer[0]
            survey.ans2 = question_set[1].question_text + " = " + answer[1]
            survey.ans3 = question_set[2].question_text + " = " + answer[2]
            survey.ans4 = question_set[3].question_text + " = " + answer[3]
            survey.ans5 = question_set[4].question_text + " = " + answer[4]
            survey.comment = comment
            survey.score = score_count
            survey.token = None
            survey.save()
            calculate_avg(survey.tutor.id, score_count)
            return HttpResponse(
                json.dumps("/survey/thank-you"),
                content_type="application/json"
            )
    else: #METHOD = GET
        try: 
            survey = Survey.objects.get(id=survey_id)
        except:
            return render(request, 'survey/no_survey.html')

        if survey.token != token:
            return render(request, 'survey/already_used.html')

        question_set = Question.objects.all()
        return render(request, 'survey/survey_page.html', {'question_set': question_set})

# REDIRECT TO THANK-YOU PAGE
def thankyou(request):
    return render(request, 'survey/thank_you.html')

# REDIRECT TO 404 PAGES
def survey_404(request, token):
    if token == 'too_long':
        return render(request, 'survey/too_long.html')
    elif token == 'no_survey':
        return render(request, 'survey/no_survey.html')
    elif token == 'already_used':
        return render(request, 'survey/already_used.html')


# CALCULATE THE TUTORS RUNNUNG AVERAGE SCORE
def calculate_avg(tutor_id, score):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    old_avg = tutor.avg_survey_score
    num_surveys = tutor.survey_count+1

    new_avg = old_avg + ((decimal.Decimal(score) - old_avg)/decimal.Decimal(num_surveys))

    tutor.avg_survey_score = new_avg
    tutor.survey_count = num_surveys
    tutor.save()