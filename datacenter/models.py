from django.db import models
import pytz
from datetime import datetime
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )
        
    def get_duration(self):
        if self.leaved_at:
            now = self.leaved_at
        else:
            now = datetime.now(pytz.timezone('Europe/Moscow'))
        duration = now - self.entered_at
        return duration.total_seconds()
        
    def format_duration(self, duration=0):
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int((duration % 3600) % 60)
        return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        
    def is_long(self):              # визит больше часа считаем долгим
        return self.get_duration() > 3600 or False
