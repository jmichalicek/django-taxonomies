from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class TaxonomyGroup(models.Model):
    """Highest level of taxonomy.  This is the name assigned to the list of
    related taxonomy items"""
    name = models.CharField(max_length=25, db_index=True)

    def __unicode__(self):
        return u'%s' %self.name

    class Meta:
        #Seems the most likely wanted ordering for anyone... and it's what I want
        ordering = ['name']

class TaxonomyItem(models.Model):
    """An actual categorization which would be assigned to some other model"""
    taxonomy_group = models.ForeignKey(TaxonomyGroup, db_index=True)
    name = models.CharField(max_length=25, db_index=True)

    def __unicode__(self):
        return u'%s' %self.name

    def get_members(self):
        """Returns a list of objects that have this item as
        part of their taxonomy.  This returns the actual models and not
        the TaxonomyMap item."""

        tmap = self.taxonomymap_set.all()
        return [i.content_object for i in tmap]

    def add_member(self, model):
        """Add a mapping of this taxa to the model.
        This is a shortcut to avoid messing with the TaxonomyMap objects
        and the extra complexities of setting the correct values for
        GenericForeignKey."""

        #Need to throw exception if model is missing, etc
        model_type = ContentType.objects.get_for_model(model)
        tmap = TaxonomyMap()
        tmap.content_type = model_type
        tmap.object_id = model.id
        tmap.taxonomy_item = self
        tmap.save()

    class Meta:
        #Again, seems the most likely wanted ordering for anyone and it's what I want
        ordering = ['name']

class TaxonomyMap(models.Model):
    """Map models to a TaxonomyItem"""
    taxonomy_item = models.ForeignKey(TaxonomyItem, db_index=True)
    content_type = models.ForeignKey(ContentType, db_index=True)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type','object_id')

    def __unicode__(self):
        return u'%s - %s' %(self.taxonomy_item, self.content_object)

class TaxonomyMember(models.Model):
    """An abstract class that models can inherit from to be taxonomized."""
    def get_taxonomies(self, group):
        """Get a list of TaxonomyItem objects for an object and TaxonomyGroup"""
        #Throw exception for missing model or group?
        type = ContentType.objects.get_for_model(self)
        tmap = TaxonomyMap.objects.filter(object_id=self.pk,
                                          taxonomy_item__taxonomy_group=group
                                          )

        return [i.taxonomy_item for i in tmap]

    def get_taxonomy_groups(self):
        """Get a list of TaxonomyGroup objects that the
        subclassed object belongs to."""
        tgroups = TaxonomyGroup.objects.filter(taxonomyitem__taxonomymap__object_id=self.pk).distinct()
        return list(tgroups)

    class Meta:
        abstract = True

## Figure out if we're in a test environment or not
## from http://www.thebitguru.com/blog/view/246-Using%20custom%20settings%20in%20django%20tests
## the last two suggestions on there are not working... python version difference, maybe?
from os import sys
TEST = False
manage_command = filter(lambda x: x.find('manage.py') != -1, sys.argv)
if len(manage_command) != 0:
  command = sys.argv.index(manage_command[0]) + 1
  if command < len(sys.argv):
    TEST = sys.argv[command] == "test"

if TEST:
    # Only load classes here if in a test environment for testing.
    # Tables for any models found here do not get created when running
    # syncdb in a live environment, only when running manage.py test
    class TaxonomyTest(TaxonomyMember):
        name = models.CharField(max_length=10)

        def __unicode__(self):
            return u'%s' %self.name
