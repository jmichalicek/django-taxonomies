"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest

from django.conf import settings
from django.core.management import call_command
from django.db.models import loading
from django import test

from taxonomy.models import *

#TODO:
# test for get_taxonomy_members and the taxonomy_members template tag
# test for TemplateItem.add_member and get_members - look at http://stackoverflow.com/questions/5097937/emulating-an-app-with-models-in-a-django-unittest

class TaxonomyTests(TestCase):
    def setUp(self):
        test_model = TaxonomyTest()
        test_model.name = 'Test Model'
        test_model.save()

        taxonomy_group = TaxonomyGroup()
        taxonomy_group.name = 'Test Group'
        taxonomy_group.save()

        taxonomy_item = TaxonomyItem()
        taxonomy_item.name = 'Test Taxonomy Item'
        taxonomy_item.taxonomy_group = taxonomy_group
        taxonomy_item.save()

        #I don't like putting this here, it should be in a test
        #but it's the only way to guarantee it'll exist when needed
        #by the other tests
        taxonomy_item.add_member(test_model)

        self.taxonomy_group = taxonomy_group
        self.taxonomy_item = taxonomy_item
        self.test_model = test_model


    def test_get_taxonomies(self):
        taxonomies = self.test_model.get_taxonomies(self.taxonomy_group)
        self.assertTrue(hasattr(taxonomies,'__iter__'))
        self.assertEqual(taxonomies[0].pk, self.taxonomy_item.pk)

    def test_get_taxonomy_groups(self):
        tgroups = self.test_model.get_taxonomy_groups()
        self.assertTrue(hasattr(tgroups,'__iter__'))
        self.assertEqual(tgroups[0].pk, self.taxonomy_group.pk)

    def test_get_members(self):
        members = self.taxonomy_item.get_members()
        self.assertTrue(hasattr(members,'__iter__'))
        self.assertEqual(members[0].pk, self.test_model.pk)

        #figure out how to test the template tag - need to parse a template

