from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from reports.serializers import GlobalProtectEventSerializer
from reports.models import GlobalProtectEvent
import logging 
logger = logging.getLogger(__name__)
import re
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic import TemplateView, ListView

class ReportView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = GlobalProtectEvent
    queryset = GlobalProtectEvent.objects.order_by('-login_date')
    template_name='report.html'
    context_object_name = 'events'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     objects_list = GlobalProtectEvent.objects.all()
    #     events = []
    #     for event in objects_list:
    #         events.append(
    #             {'user':event.user,
    #             'login_date':event.login_date,
    #             'logout_date':event.logout_date,
    #             'duration':  event.logout_date - event.login_date if (event.logout_date and event.login_date) else ''
    #             })
    #     # Add in a QuerySet of all the books
    #     logger.error(events)
    #     context['events'] = events
    #     return context

class GlobalProtectEventViewSet(viewsets.ModelViewSet):
    queryset = GlobalProtectEvent.objects.all()
    serializer_class = GlobalProtectEventSerializer

    def create(self, request):
        # do your thing here
        message = request.body.decode('utf-8')
        (event, user) = re.compile('GlobalProtect gateway user (login|logout) succeeded. .*User name: ([a-zA-Z0-9]+),').search(message).groups()
        if(event == 'login'):
            e = GlobalProtectEvent(login_date=timezone.now(), login_event=message, user=user)
            e.save()
        if(event == 'logout'):
            try:
                e = GlobalProtectEvent.objects.filter(user=user, logout_date=None).order_by('-login_date')[0]
                e.logout_date = timezone.now()
                e.logout_event = message
                e.save()
            except IndexError: # no matching login event
                e = GlobalProtectEvent(logout_date=timezone.now(), logout_event=message, user=user)
                e.save()
        return Response(status=status.HTTP_200_OK)


# login = "GlobalProtect gateway user login succeeded. Login from: 192.168.55.131, Source region: 192.168.0.0-192.168.255.255, User name: gkujawsk, Client OS version: Microsoft Windows 10 Pro , 64-bit."
# logout = "GlobalProtect gateway user logout succeeded. User name: gkujawsk, Client OS version: Microsoft Windows 10 Pro , 64-bit, Reason: client logout."
# (event, username) = re.compile('GlobalProtect gateway user (login|logout) succeeded. .*User name: ([a-zA-Z0-9]+),').search(login).groups()