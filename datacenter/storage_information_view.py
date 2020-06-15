from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from datetime import datetime
import pytz


def format_duration(d=0):
    h = int(d // 3600)
    m = int((d % 3600) // 60)
    s = int((d % 3600) % 60)
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)
    
def storage_information_view(request):
    # Программируем здесь
    visits = Visit.objects.filter(leaved_at=None)
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    non_closed_visits = []
    for v in visits:
        non_closed_visits.append(
            {
                "who_entered": v.passcard.owner_name,
                "entered_at": localtime(v.entered_at),
                "duration": format_duration(v.get_duration()),
            })

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
