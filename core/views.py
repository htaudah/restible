from django.shortcuts import render

from oauth2_provider.views.generic import ProtectedResourceView
from django.views.generic import View
from django.http import HttpResponse, JsonResponse

from django.conf import settings

import paramiko
import json

# Create your views here.
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(settings.ANSIBLE_HOST, port=22, username=settings.ANSIBLE_USER, password=settings.ANSIBLE_PASSWORD)
        client.exec_command("echo hey > /tmp/echi")
        return HttpResponse('Hello, OAuth2!')

    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        # userid = request_data['userid']
        # subnet = request_data['subnet']
        # client = paramiko.SSHClient()
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.connect(settings.ANSIBLE_HOST, port=22, username=settings.ANSIBLE_USER, password=settings.ANSIBLE_PASSWORD)
        # client.exec_command("cd %s; ./run_playbooks.sh" % (settings.ANSIBLE_PATH,))
        # return JsonResponse({'status':'running'})
        return JsonResponse(request_data)

class HealthEndpoint(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('API is healthy')

