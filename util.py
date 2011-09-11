from models import *
from django.contrib.contenttypes.models import ContentType

def get_taxonomy_for_object(model, group):
    """Get a list of TaxonomyItem objects for an object and TaxonomyGroup"""
    #Throw exception for missing model or group

    type = ContentType.objects.get_for_model(model)
    tmap = TaxonomyMap.objects.filter(object_id=model.pk,
                                      taxonomy_item__taxonomy_type=group
                                      )

    return [i.taxonomy_item for i in tmap]

def get_objects_for_taxonomy(taxonomy):
    pass
