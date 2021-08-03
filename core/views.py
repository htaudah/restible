from django.shortcuts import render

from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse

from django.conf import settings

import paramiko

# Create your views here.
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(settings.ANSIBLE_HOST, port=22, username=settings.ANSIBLE_USER, password=settings.ANSIBLE_PASSWORD)
        client.exec_command("echo hey > /tmp/echi")
        return HttpResponse('Hello, OAuth2!')
