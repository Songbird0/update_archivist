import pathlib

import django.http
import django.views

# CONSTANTS

USER_HOME = pathlib.Path.home()
UPDATER_HOME = USER_HOME / 'UpdateArchivist'
DEPLOYED_UPDATE_DIRECTORY = UPDATER_HOME / 'production'
SUBMITTED_UPDATE_DIRECTORY = UPDATER_HOME / 'submitted'

def greetings(request: django.http.HttpRequest) -> django.http.HttpResponse:
    return django.http.HttpResponse('Hello yorld!', content_type='text/plain')

def build_project_root(*args):
    import os
    path_list = list(args)
    for path in path_list:
        if not issubclass(path.__class__, os.PathLike):
            raise Exception('One of these elements is NOT a Path-Like object.')
        else:
            try:
                path.mkdir(mode=600, parents=True)
                print("'{}' was created.".format(path))
            except(FileExistsError):
                print("'{}' already exists. OK.".format(path))

build_project_root(DEPLOYED_UPDATE_DIRECTORY, SUBMITTED_UPDATE_DIRECTORY)

class FileListView(django.views.View):
    """Returns the update file list.

    All file sums are generated with blake2b."""
    def get(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        pass


class MissingFileView(django.views.View):

    def post(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        pass
