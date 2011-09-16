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
from django.template import Template, Context, Parser

from mock import patch, Mock

from taxonomy.models import *

# Idea to use mock for testing template tags from the links below
# http://techblog.ironfroggy.com/2008/10/how-to-test-django-template-tags-part-1.html
# http://techblog.ironfroggy.com/2008/10/how-to-test-django-template-tags-part-2.html

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

        self.group_name = 'Test Group'
        self.model_name = 'Test Model'
        self.item_name = 'Test Taxonomy Item'

        self.taxonomy_group = taxonomy_group
        self.taxonomy_item = taxonomy_item
        self.test_model = test_model


    def test_get_taxonomies(self):
        tt = TaxonomyTest.objects.get(name=self.model_name)
        taxonomies = tt.get_taxonomies(self.taxonomy_group)
        self.assertTrue(hasattr(taxonomies,'__iter__'))
        self.assertEqual(taxonomies[0].pk, self.taxonomy_item.pk)

    def test_get_taxonomy_groups(self):
        tt = TaxonomyTest.objects.get(name=self.model_name)
        tgroups = tt.get_taxonomy_groups()
        self.assertTrue(hasattr(tgroups,'__iter__'))
        self.assertEqual(tgroups[0].pk, self.taxonomy_group.pk)

    def test_get_members(self):
        ti = TaxonomyItem.objects.get(name=self.item_name)
        members = ti.get_members()
        self.assertTrue(hasattr(members,'__iter__'))
        self.assertEqual(members[0].pk, self.test_model.pk)

    def test_get_members_tag(self):
        """This tests the get_taxonomy_members method which is directly called by 
        the get_members tag and so tests instantion of the TaxonomyMembers object.
        It also tests to make sure the TaxonomyMembers' render() method works"""

        parser = Parser(None)
        token = Mock(spec=['split_contents'])
        
        token.split_contents.return_value = ('get_members', self.taxonomy_group.name,
                                             self.taxonomy_item.name)


        from templatetags.taxonomy_tags import get_taxonomy_members
        node = get_taxonomy_members(parser,token)
        self.assertEqual(node.taxonomy_group, self.taxonomy_group.name)
        self.assertEqual(node.taxonomy_item, self.taxonomy_item.name)

        # It feels like this part below should be its own test
        # but the above needs to be done to test it, so might as well
        # just consider it all one test
        c = Context()
        node.render(c)
        self.assertTrue(hasattr(c['members'],'__iter__'))
        self.assertEqual(c['members'][0].pk, self.test_model.pk)

