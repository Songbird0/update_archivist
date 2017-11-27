import django.http
import django.views

def greetings(request: django.http.HttpRequest) -> django.http.HttpResponse:
    return django.http.HttpResponse('Hello yorld!', content_type='text/plain')

class FileListView(django.views.View):
    """Returns the update file list.

    All file sums are generated with blake2b."""
    def get(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        pass


class MissingFileView(django.views.View):

    def post(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        pass
