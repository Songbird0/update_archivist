#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import pathlib
import sys

# CONSTANTS
USER_HOME = pathlib.Path.home()
UPDATER_HOME = USER_HOME / 'UpdateArchivist'
DEPLOYED_UPDATE_DIRECTORY = UPDATER_HOME / 'production'
SUBMITTED_UPDATE_DIRECTORY = UPDATER_HOME / 'submitted'
LOGGING_CONFIGURATION = {
    'format': '[{asctime}][{levelname}]:{message}',
    'datefmt': '%d/%m/%Y (%I:%M:%S) %p',
    'style': '{',
    'level': logging.DEBUG,
    'stream': sys.stdout
    }
logging.basicConfig(**LOGGING_CONFIGURATION)
LOGGER = logging.getLogger(__name__)

def build_project_root(*args):
    import os
    path_list = list(args)
    for path in path_list:
        if not issubclass(path.__class__, os.PathLike):
            raise Exception('One of these elements is NOT a Path-Like object.')
        else:
            try:
                path.mkdir(mode=600, parents=True)
                LOGGER.info("'{}' was created.".format(path))
            except(FileExistsError):
                LOGGER.info("'{}' already exists. OK.".format(path))

def its_time_to_update():
    # get SUBMITTED_UPDATE_DIRECTORY files/directories
    number_of_directories = sum(1 for _ in SUBMITTED_UPDATE_DIRECTORY.iterdir())
    if number_of_directories > 0:
        import zipfile
        for file in SUBMITTED_UPDATE_DIRECTORY.iterdir():
            if not zipfile.is_zipfile(file):
                LOGGER.warning("The updater does support .zip resources only at this time.\n"
                               "Targeted file: {}".format(file))
            else:
                # open and check the archive integrity (it must contain a single root directory).
                # create temp directory
                temp_directory = SUBMITTED_UPDATE_DIRECTORY / 'temp_check'
                temp_directory.mkdir(mode=600, exist_ok=True)
                # extract the stuff
                with zipfile.ZipFile(file) as compressed_update:
                    compressed_update.extractall(temp_directory)
                    if sum(1 for potential_dir in temp_directory.iterdir() if potential_dir.is_dir()) > 1:
                        # raise an exception or log it and exit to avoid multiple
                        # root directories.
                        ...
    else:
        return False


