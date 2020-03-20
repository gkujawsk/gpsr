from django.db import models
from django.utils import timezone

class GlobalProtectEvent(models.Model):
	login_event = models.CharField(max_length=1024, null=True)
	logout_event = models.CharField(max_length=1024, null=True)
	user = models.CharField(max_length=128, null=False)
	login_date = models.DateTimeField(null=True)
	logout_date = models.DateTimeField(null=True)