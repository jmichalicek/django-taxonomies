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
    """This class adds the taxonomy/test app to installed_apps
    to use the model there for test cases."""

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

        #def test_create_taxonomized_item(self):
        #taxonomy_item = TaxonomyItem.objects.get(name='Test Taxonomy Item')
        #ntaxonomy_item.add_member(test_model)

    def test_get_taxonomies(self):
        taxonomies = self.test_model.get_taxonomies(self.taxonomy_group)

        self.assertIsInstance(taxonomies, list)

#    def test_get_taxonomy_groups(self):
#        test_model = TaxonomyTest.objects.get(pk=1)
#        test_model.get_taxonomy_groups()

#    def test_get_members(self):
#        taxonomy_item = TaxonomyItem.objects.get(name='Test Taxonomy Item')
#        taxonomy_item.get_members()

        #figure out how to test the template tag - need to parse a template

