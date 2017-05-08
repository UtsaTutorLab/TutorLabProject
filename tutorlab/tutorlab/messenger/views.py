from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.views.generic.detail import DetailView
from .models import Room, Message
from ta_tutor.models import Tutor
from django.conf import settings 
from django.core import signing
from student.models import Queue
from survey.models import Survey
from pusher import pusher

#def chat_room(request, label):
def chat_room(request, token):
	# If the room with the given label doesn't exist, automatically create it upon first visit.
	# room, created = Room.objects.get_or_create(label=label)
	try:
		room_id = signing.loads(token,
                            max_age = settings.ROOM_TOKEN_EXPIRES,
                            salt=settings.SECRET_KEY)
	except signing.BadSignature:
		return HttpResponse("Incorrect signature")
	else:
		try:
			room = Room.objects.get(id=room_id)
		except ObjectDoesNotExist:
			return HttpResponse("Room doesn't exist")
		if room.token != token:
			return HttpResponse("Request already being handled")
	
	# We want to show the last 50 messages, orded by most-recent-last
	messages = reversed(room.messages.order_by('-timestamp')[:50])

	#Pusher Client Initialization
	pusher_client = pusher.Pusher(app_id=settings.PUSHER_APP_ID,
									key=settings.PUSHER_KEY,
									secret=settings.PUSHER_SECRET)

	# Let template know if user is a tutor
	isTutor = False
	# student = Queue.objects.create(abc123="000000",chair="00",classID="0000.00",inSession=True,)
	# tutor = Tutor.objects.create(name="000000")
	# student = None
	# tutor = None

	if request.user.groups.filter(name='Student'):
		whole_name = ""
		try:
			whole_name = str(request.user.get_full_name())
		except:
			whole_name = request.user

		try:
			# Create new Queue object
			Queue.objects.create(abc123=request.user, inSession=0, classID=0, chair=000, isChat=1, chat_token=token)
		except IntegrityError as err:
			print("THIS IS THE ERROR" + str(err))

		student = Queue.objects.get(abc123=request.user)
		student.whole_name = whole_name
		student.save()
		
		# Update tutor page queue
		pusher_client.trigger(u'ch1', u'enqueue', {u'label': request.user.username})

	if request.user.groups.filter(name="Tutor"):
		isTutor = True
		try:
			room = Room.objects.get(token=token)
			student = Queue.objects.get(abc123=room.label)
			student.inSession = 1
			student.save()
			pusher_client.trigger(u'ch1', u'enqueue', {})
			
		except ObjectDoesNotExist:
			return HttpResponseRedirect('../../ta_tutor')

	
		
	return render(request, "messenger/msg.html", {'room': room, 'messages': messages, 'isTutor':isTutor})

# give url a token for security

def gen_token(request, label):

	room = Room.objects.create(label=label)

	token = signing.dumps(room.id, salt=settings.SECRET_KEY)
	room.token = token
	room.save()

	try:
		# Create new Queue object
		student = Queue(abc123=request.user, inSession=0, classID=0, chair=000, isChat=1, chat_token=token )
		student.save()
	except IntegrityError:
		pass
	else:
		#Pusher Client Initialization
		pusher_client = pusher.Pusher(app_id=settings.PUSHER_APP_ID,
										key=settings.PUSHER_KEY,
										secret=settings.PUSHER_SECRET)
		pusher_client.trigger(u'ch1', u'enqueue', {u'label': request.user.username})

	return HttpResponseRedirect("../"+token)

	# return HttpResponse("Okay")

	# return render(request, "messenger/msg.html", {'token':token})
	# chat_room(request, token)