from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Queue
from survey.models import Choice, Question, Survey
import json, socket, sys, threading

@receiver(post_save, sender=Queue)
def send_in_session(instance, **kwargs):
    '''
    '''
    if instance.host != "none": # change to None
        t = threading.Thread(
            target=send_message,
            args=(instance.host, instance.port, "in session"),
            daemon=True
        )
        t.start()

@receiver(post_delete, sender=Queue)
def send_update_queue(**kwargs):
    '''
    '''
    queue_list = Queue.objects.all()
    for student in queue_list:
        if student.host != "none": #change to None
            num = Queue.objects.filter(id__lte = student.id).count()
            t = threading.Thread(
                target=send_message,
                args=(student.host, student.port, "queue update"), 
                kwargs={'position':num},
                daemon=True
            )
            t.start()

@receiver(post_delete, sender=Queue)
def send_end_session(instance, **kwargs):
    '''
    '''
    if instance.host != "none": # change to None
        surveys = Survey.objects.filter(student=instance).order_by('-id')
        survey = surveys[0]
        quest_list = Question.objects.all()
        questions = []
        for q in quest_list:
            new_question = []
            new_question.append(q.question_text)
            scale = Choice.objects.get(id=q.scale_choice.id)
            new_question.append(scale.low)
            new_question.append(scale.high)
            questions.append(new_question)

        t = threading.Thread(
            target=send_message,
            args=(instance.host, instance.port, "end session"),
            kwargs={'questions':questions, 'survey_token':survey.token},
            daemon=True
        )
        t.start()

def send_message(host, port, msg, **kwargs):
    '''
    '''
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # connection to hostname on the port.
    print("Connecting to host = "+ host, "port = "+str(port))
    s.connect((host, int(port)))                               

    # Receive no more than 1024 bytes
    get = s.recv(1024)                                     
    getmsg = json.loads(get.decode('ascii'))
    try:
        if getmsg['app_key'] != settings.SECRET_KEY:
            print('App Key does not match, closing connection')
            s.close()
    except KeyError:
        print('Data does not have App_Key field')
        s.close()

    if msg == "end session":
        sndmsg={'app_key':settings.SECRET_KEY, 'bool':"True", 'message':msg, 'questions':kwargs['questions'], 'survey_token':kwargs['survey_token']}
    elif msg == "queue update":
        sndmsg={'app_key':settings.SECRET_KEY, 'bool':"True", 'message':msg, 'position':kwargs['position']}
    else:    
        sndmsg={'app_key':settings.SECRET_KEY, 'bool':"True", 'message':msg}

    s.send(json.dumps(sndmsg).encode('ascii'))
    s.close()
