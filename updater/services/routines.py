#!/usr/bin/python
# -*- coding: utf-8 -*-

# Std

import hashlib
import logging
import pathlib
import shutil
import sys
import zipfile

# Internal

from .. import models

# CONSTANTS
USER_HOME = pathlib.Path.home()
UPDATER_HOME = USER_HOME / 'UpdateArchivist'
DEPLOYED_UPDATE_DIRECTORY = UPDATER_HOME / 'production'
SUBMITTED_UPDATE_DIRECTORY = UPDATER_HOME / 'submitted'
LOGGING_CONFIGURATION = {
    'format': '|{name}|[{asctime}][{levelname}]:{message}',
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

def remove_suffix(your_string: str, suffix_to_remove: str) -> str:
    if your_string.endswith(suffix_to_remove):
        suffix_index = your_string.rindex(suffix_to_remove)
        return your_string[:suffix_index]
    else:
        raise Exception('Your string is not suffixed by "{}".'.format(suffix_to_remove))

def its_time_to_update(submitted_update_directory=SUBMITTED_UPDATE_DIRECTORY):
    """Returns the zip path if there's a new update to apply, `None` otherwise.

    While it is running, this function will update the `zipped_scaffolding_sum` field to
    identify the production version and the new updates.

    **Note**: `its_time_to_update` will pick the first .zip archive returned by `iterdir()` method.
    """
    # get SUBMITTED_UPDATE_DIRECTORY files/directories
    number_of_directories = sum(1 for _ in submitted_update_directory.iterdir())
    if number_of_directories > 0:
        for file in submitted_update_directory.iterdir():
            if not zipfile.is_zipfile(file):
                LOGGER.warning("The updater does support .zip resources only at this time.\n"
                               "Targeted file: {}".format(file))
            else:
                # open and check the archive integrity (it must contain one single root directory).
                # create temp directory
                temp_directory = submitted_update_directory / 'temp_check'
                temp_directory.mkdir(mode=600, exist_ok=True)
                # extract the stuff
                with zipfile.ZipFile(file) as compressed_update:
                    compressed_update.extractall(temp_directory)
                number_of_root_directories = sum(
                    1 for potential_dir in temp_directory.iterdir() if potential_dir.is_dir())
                if number_of_root_directories == 0:
                    try:
                        shutil.rmtree(temp_directory)
                    except Exception as e:
                        LOGGER.error(e)
                    # raise an exception or log it and exit to avoid multiple
                    # root directories.
                    raise Exception(
                        '`{}` is empty. Your zip should contain a root directory.'.format(compressed_update))
                if number_of_root_directories > 1:
                    try:
                        shutil.rmtree(temp_directory)
                    except Exception as e:
                        LOGGER.error(e)
                    raise Exception(
                        'Your archive contains too many root directories. The updater supports one single root directory.')
                file_content = file.read_bytes()
                zip_sum = hashlib.blake2b(file_content).hexdigest()
                try:
                    scaffolding_sum = models.ScaffoldingState.objects.get(id=1)
                    if scaffolding_sum.zipped_scaffolding_sum == zip_sum:
                        return None
                    else:
                        scaffolding_sum.zipped_scaffolding_sum = zip_sum
                        scaffolding_sum.save()
                        return file
                except models.ScaffoldingState.DoesNotExist:
                    # Matches when the updater is running for the first time.
                    if file.suffix:
                        first_sum = models.ScaffoldingState.objects.create(
                            project_name=remove_suffix(file, file.suffix), zipped_scaffolding_sum=zip_sum)
                    else:
                        first_sum = models.ScaffoldingState.objects.create(
                            project_name=file.name, zipped_scaffolding_sum=zip_sum)
                    first_sum.save()
                    return file
                finally:
                    try:
                        shutil.rmtree(temp_directory)
                    except Exception as e:
                        LOGGER.error(e)
    else:
        return None
