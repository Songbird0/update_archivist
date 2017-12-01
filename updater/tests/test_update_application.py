#!/usr/bin/python
# -*- coding: utf-8 -*-

# Std

# Third party

import django.test

# Internal

import updater.models
import updater.services.update_application

class EmptyDatabase(django.test.TestCase):
    def setUp(self):
        print('Nothing to do!')

    def test_database_if_empty(self):
        self.assertTrue(updater.services.update_application.database_is_empty(), 'Oops! The database is not empty.')

class FilledDatabase(django.test.TestCase):
    def setUp(self):
        updater.models.RemovedFile.objects.create(relative_path='project_root/file/to/remove')
        updater.models.AddedFile.objects.create(relative_path='project_root/file/to/create')
        updater.models.ModifiedFile.objects.create(relative_path='project_root/modified/file', checksum='0xCAFEBABE')
        updater.models.UnmodifiedFile.objects.create(relative_path='project_root/unmodified/file', checksum='0xDEADBEEF')

    def test_database_if_empty(self):
        self.assertFalse(updater.services.update_application.database_is_empty(), 'Oops! The database is empty.')
