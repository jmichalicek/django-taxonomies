from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class TaxonomyGroup(models.Model):
    """Highest level of taxonomy.  This is the name assigned to the list of
    related taxonomy items"""
    name = models.CharField(max_length=25, db_index=True)

    def __unicode__(self):
        return u'%s' %self.name

class TaxonomyItem(models.Model):
    """An actual categorization which would be assigned to some other model"""
    taxonomy_group = models.ForeignKey(TaxonomyGroup, db_index=True)
    name = models.CharField(max_length=25, db_index=True)

    def __unicode__(self):
        return u'%s' %self.name

    def get_items(self):
        """Returns a list of objects that have this item as
        part of their taxonomy.  This returns the actual models and not
        the TaxonomyMap item."""

        tmap = self.taxonomymap_set.all()
        return [i.content_object for i in tmap]

    def add_item(self, model):
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
        return tgroups

    class Meta:
        abstract = True
