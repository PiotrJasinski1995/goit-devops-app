from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello from Django CI/CD app!")
