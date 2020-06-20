from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
    

def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in visits:
        if True in tuple(vis.is_long() for vis in Visit.objects.filter(passcard=visit.passcard)):
            is_strange = True
        else:
            is_strange = False
        non_closed_visits.append(
            {
                "who_entered": visit.passcard.owner_name,
                "entered_at": localtime(visit.entered_at),
                "duration": visit.format_duration(visit.get_duration()),
                "is_strange": is_strange
            })
    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
