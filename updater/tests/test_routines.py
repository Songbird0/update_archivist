#!/usr/bin/python
# -*- coding: utf-8 -*-

# Std

import hashlib
import pathlib

import django.test

import updater.services.routines
from updater import models

# Third party
# Internal

# CONSTANTS

SUM_TEST_DIRECTORY = pathlib.Path.cwd() / 'updater' / 'tests' / 'test_routines_files' / 'sum'
IDENTICAL_SUM_DIRECTORY = SUM_TEST_DIRECTORY / 'identical'
DIFFERENT_SUM_DIRECTORY = SUM_TEST_DIRECTORY / 'different'


# Checker

class IdenticalSumTest(django.test.TestCase):
    """Represents a comparison between two identical blake2b sum.

    Here, the scaffolding project sum should be identical to the archive sum."""
    SUM = '4c71a3bd7b1d7951e52edf7160094a980f808633eed1140c5a476ecade2793d502f63289b855a1fa6f0520dcfd2037094282c1df7938cc0ffb813a6651a71527'
    def setUp(self):
        models.ScaffoldingState.objects.create(zipped_scaffolding_sum=self.SUM)
        updater.services.routines.build_project_root(IDENTICAL_SUM_DIRECTORY, IDENTICAL_SUM_DIRECTORY / 'production')

    def test_against_identical_sum(self):
        zip_file = IDENTICAL_SUM_DIRECTORY / 'identical_sum_test.zip'
        self.assertTrue(zip_file.exists(), 'Oops. "{}" doesn\'t exist. Please create it.'.format(zip_file))
        zip_file_sum = hashlib.blake2b(zip_file.read_bytes()).hexdigest()
        # Should not throw AssertionError object.
        self.assertTrue(models.ScaffoldingState.objects.filter(zipped_scaffolding_sum=zip_file_sum).exists(), 'The last scaffolding sum isn\'t equal to \n{0} but instead \n{1}'.format(zip_file_sum, self.SUM))
        self.assertTrue(updater.services.routines.its_time_to_update(submitted_update_directory=IDENTICAL_SUM_DIRECTORY) is None)

class DifferentSumTest(django.test.TestCase):
    """Represents a comparison between two different blake2b sum.

    Here, the scaffolding project sum should NOT be identical to the archive sum."""
    SUM = '84d5579f68aafc73185fc2d3e0413d6f1e2dca129515e351df4a5bc2f90b05d51442d8bc4735ed10bf08765fe4815b6b410461cf04b044add4eb35f0e5bc4a4a'
    def setUp(self):
        models.ScaffoldingState.objects.create(zipped_scaffolding_sum=self.SUM)
        updater.services.routines.build_project_root(DIFFERENT_SUM_DIRECTORY, DIFFERENT_SUM_DIRECTORY / 'production')

    def test_against_different_sum(self):
        zip_file = DIFFERENT_SUM_DIRECTORY / 'different_sum_test.zip'
        self.assertTrue(zip_file.exists(), 'Oops. "{}" doesn\'t exist. Please create it.'.format(zip_file))
        zip_file_sum = hashlib.blake2b(zip_file.read_bytes()).hexdigest()
        # Should not throw AssertionError object.
        self.assertFalse(models.ScaffoldingState.objects.filter(zipped_scaffolding_sum=zip_file_sum).exists(), 'The last scaffolding sum ({0}) should NOT be equal to zip file sum ({1}).'.format(self.SUM, zip_file_sum))
        self.assertTrue(updater.services.routines.its_time_to_update(submitted_update_directory=DIFFERENT_SUM_DIRECTORY) is not None)
