from django.shortcuts import render

from oauth2_provider.views.generic import ProtectedResourceView
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from django.conf import settings

import paramiko
import json
import shlex

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
        #arg_string = ""
        request_params = {}
        for key in request_data:
            if key == 'playbooks':
                continue
            #arg_string += " %s=%s" % (key, request_data[key])
            request_params[key] = request_data[key]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(settings.ANSIBLE_HOST, port=22, username=settings.ANSIBLE_USER, password=settings.ANSIBLE_PASSWORD)
        if not ('playbooks' in request_data):
            return JsonResponse({'error': 'No playbooks were specified in request body'}, status=400)
        for playbook in request_data['playbooks']:
            client.exec_command("%s/run_playbooks.sh %s %s" % (settings.ANSIBLE_PATH, playbook, shlex.quote(json.dumps(request_params))))
        return JsonResponse({'status':'running'})

class HealthEndpoint(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('API is healthy')
