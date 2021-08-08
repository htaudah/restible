from django.shortcuts import render

from oauth2_provider.views.generic import ProtectedResourceView
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
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

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        arg_string = ""
        for key in request_data:
            if key == 'playbooks':
                continue
            arg_string += " %s=%s" % (key, request_data[key])
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(settings.ANSIBLE_HOST, port=22, username=settings.ANSIBLE_USER, password=settings.ANSIBLE_PASSWORD)
        client.exec_command("cd %s; ./run_playbooks.sh %s" % (settings.ANSIBLE_PATH, arg_string))
        return JsonResponse({'status':'running'})

class HealthEndpoint(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('API is healthy')

