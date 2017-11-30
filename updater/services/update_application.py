#!/usr/bin/python
# -*- coding: utf-8 -*-

# Std

import logging
import zipfile
import hashlib
import pathlib

# Third party

# Internal

from . import routines

# CONSTANTS
LOGGER = logging.getLogger(__name__)


class UpdateManager:
    """Compares the last scaffolding state to the new update and records the files state.

    The files state can be:

    - Removed (no blake2bsum supplied);
    - Added (no blake2bsum supplied);
    - Modified (blake2sum is supplied);
    - Unmodified (blake2sum is supplied).

    > Why removed and added files should not have blake2sum ?

    It's simple: `UpdateManager` is the boss. All clients receive the order to add and/or remove all spotted files, whatever their sum.
    Obviously, modified and unmodified files were supplied with their blake2sum to perform some security checks, among other things.
    """

    scaffolding_json_representation = ...
    """The project files, in json."""

    def __init__(self):
        routines.build_project_root()
        zip_path = routines.its_time_to_update()
        self.apply_update(zip_path)

    def apply_update(self, update_archive_path, update_directory=routines.SUBMITTED_UPDATE_DIRECTORY,
                     production_directory=routines.DEPLOYED_UPDATE_DIRECTORY):
        if update_archive_path is not None:
            LOGGER.info("Update available, yay!")

        else:
            LOGGER.info("There's no update to apply for now.")

    def record_modifications(self):
        """Compares the last scaffolding state to the new update and records the files state.

        The new scaffolding is returned in json."""
        pass

    def update_scaffolding(self):
        """Updates the database models to dispatch the new project state."""
        pass

    def create_relative_path(initial_path: pathlib.Path, new_root: str) -> pathlib.Path:
        """Creates a new path from the initial path.
        Example:
        your_path = pathlib.Path('/foo/bar/baz/bang')
        create_relative_path(your_path, 'bar') returns -> Windows|UnixPath('bar/baz/bang')
        If `new_root` does not exist, `create_relative_path` will return `None`.
        """
        stringified_initial_path = initial_path.__str__()
        new_root_index = stringified_initial_path.index(new_root)
        if new_root_index > 0:
            return pathlib.Path(stringified_initial_path[new_root_index:])
        else:
            return None
