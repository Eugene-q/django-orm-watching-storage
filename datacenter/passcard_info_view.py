from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    this_passcard_visits = []
    for v in Visit.objects.filter(passcard=passcard):
        this_passcard_visits.append(
            {
                "entered_at": localtime(v.entered_at),
                "duration": v.format_duration(v.get_duration()),
                "is_strange": v.is_long(),
            }
        )
    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
