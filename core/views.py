from django.shortcuts import render

# Create your views here.
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')
