from django.contrib import admin
from django.contrib.contenttypes import generic
from models import *

class TaxonomyItemInline(admin.StackedInline):
    model = TaxonomyItem
    extra = 1

class TaxonomyMapInline(generic.GenericStackedInline):
    model = TaxonomyMap
    extra = 1

class TaxonomyGroupAdmin(admin.ModelAdmin):
    inlines = [TaxonomyItemInline]

class TaxonomyItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'taxonomy_group')
    list_filter = ('taxonomy_group',)

admin.site.register(TaxonomyGroup, TaxonomyGroupAdmin)
admin.site.register(TaxonomyItem, TaxonomyItemAdmin)
admin.site.register(TaxonomyMap)
