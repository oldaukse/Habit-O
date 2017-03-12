from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import date
import json

# Habit model
class Habit(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	description = models.TextField()
	# setting auto_now_add will cause the created field to be not editable
	# unsure if this should be the case...
	created = models.DateField(default=date.today)
	days = models.TextField(max_length=128, default={})
	slug = models.SlugField()
	
	# Set as unique the combination title + user (a user cannot create two habits with the same title)
	class Meta:
		unique_together = ('user', 'title')
		
	# Returns days as a dictionary.
	# A dictionary cannot be directly stored in the database, 
	# so the value of days field must be parsed to a json object in order to be used
	def getDaysList(self):
		return json.loads(self.days)
	
	# Checks days starting from creation date until now
	# and sets empty days to 0
	def checkDays(self):
		days = json.loads(self.days)
		start_date = self.created
		now_date = date.today()
		diff_days = (now_date - start_date).days
		for d in range(1, diff_days + 1):
			if str(d) not in days:
				days[str(d)] = 0
		self.days = json.dumps(days)
		self.save()
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Habit, self).save(*args, **kwargs)
		
	def __str__(self):
		return self.title
	
	def __unicode__(self):
		return self.title
