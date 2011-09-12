"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


#TODO:
# test for get_taxonomy_members and the taxonomy_members template tag
# test for TemplateItem.add_member and get_members - look at http://stackoverflow.com/questions/5097937/emulating-an-app-with-models-in-a-django-unittest
