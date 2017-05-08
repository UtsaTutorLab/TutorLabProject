from django.db import models
from django.utils import timezone

class Room(models.Model):
	name=models.TextField()
	label=models.SlugField(unique=True)
	studentConnected=models.BooleanField(default=False)
	tutorConnected=models.BooleanField(default=False)
	token = models.CharField(max_length=150, null=True)

	def __unicode__(self):
		return self.label

class Message(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
	handle = models.TextField()
	message = models.TextField()
	timestamp = models.DateTimeField(default=timezone.now, db_index=True)

	def __unicode__(self):
		return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

	@property
	def formatted_timestamp(self):
		return self.timestamp.strftime('%b %-d %-I:%M %p')

	def as_dict(self):
		return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}

    
