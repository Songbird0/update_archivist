import django.http


def greetings(request: django.http.HttpRequest) -> django.http.HttpResponse:
    return django.http.HttpResponse('Hello yorld!', content_type='text/plain')

