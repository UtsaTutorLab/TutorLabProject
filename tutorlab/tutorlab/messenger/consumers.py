from channels import Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from .models import Room, Message
from student.models import Queue
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from pusher import pusher
import time
import json

pusher_client = pusher.Pusher(app_id=settings.PUSHER_APP_ID,
                        key=settings.PUSHER_KEY,
                        secret=settings.PUSHER_SECRET)

@channel_session_user_from_http
def ws_connect(message):
	#prefix, label = message['path'].strip('/').split('/')
	token = message['path'][5:-1].strip('/')
	room = Room.objects.get(token=token)
	label = room.label
	Group('chat-'+label).add(message.reply_channel)
	message.channel_session['room'] = room.token
	m = room.messages.create(handle=message.user.username, message="has connected!")
	Group('chat-'+label).send({'text': json.dumps(m.as_dict())})

	#Test if student or tutor and mark as connected to room
	if message.user.groups.filter(name='Students'):
		room.studentConnected = True
	if message.user.groups.filter(name='TA/Tutors'):
		room.tutorConnected = True
	room.save()

@channel_session_user
def ws_receive(message):
	token = message.channel_session['room']
	room = Room.objects.get(token=token)
	label = room.label
	data = json.loads(message['text'])
	#m = room.messages.create(handle=data['handle'], message=data['message'])
	m = room.messages.create(handle=message.user.username, message=data['message'])
	Group('chat-'+label).send({'text': json.dumps(m.as_dict())})

@channel_session_user
def ws_disconnect(message):
	# tutor = Tutor.objects.get(name=message.user.get_full_name())
	# student = Queue.objects.get()
	# if request.user.groups.filter(name='Tutor'):
	# 	# CREATE NEW SURVEY OBJECT 
	# 	survey = Survey.create(tutor)
	# 	survey.student = student.abc123
	# 	survey.save()

		# # CREATE URL TOKEN
		# token = signing.dumps(survey.id, salt=settings.SECRET_KEY)
		# survey.token = token
		# survey.save()

	token = message.channel_session['room']
	room = Room.objects.get(token=token)
	label = room.label
	#if message.user.groups.filter(name='Students'):
	m = room.messages.create(handle=message.user.username, message="has disconnected")
	#else:
		#m = room.messages.create(handle=message.user.username, message="We were happy to help you today. Follow the link below to answer a short survey about your experience today. Thank You!<br><a href='>Survey</a>")

	Group('chat-'+label).send({'text': json.dumps(m.as_dict())})
	#Test if student or tutor and mark as not connected to room
	if message.user.groups.filter(name='Student'):
		room.studentConnected = False
	if message.user.groups.filter(name='Tutor'):
		room.tutorConnected = False

	room.save()

	if room.studentConnected is False and room.tutorConnected is False:
		Group('chat-'+label).discard(message.reply_channel)
		room.delete()
		cur_queue = Queue.objects.get(abc123 = label)
		cur_queue.delete()
		pusher_client.trigger(u'ch1',u'enqueue',{u'msg':'somehting else'})