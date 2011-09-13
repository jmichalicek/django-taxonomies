from django import template

from taxonomy.models import *

register = template.Library()

def get_taxonomy_members(parser, token):
    try:
        bits = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents.split()[0]
            )

    if len(bits) == 3:
        #sort of duplicate due to default value on TaxonomyMembers.__init__()
        var_name = "members"
    elif len(bits) == 5 and bits[3] == "as":
        var_name = bits[4]

    return TaxonomyMembers(bits[1], bits[2], var_name)

class TaxonomyMembers(template.Node):
    def __init__(self, taxonomy_group, taxonomy_item, var_name="members"):
        self.taxonomy_item_name = template.Variable(taxonomy_item)
        self.taxonomy_group_name = template.Variable(taxonomy_group)
        self.variable_name = var_name

    def render(self, context):
        resolved_name = self.taxonomy_item_name.resolve(context)
        resolved_group = self.taxonomy_group_name.resolve(context)
        taxonomy_item = TaxonomyItem.objects.get(name=resolved_name,
                                                 taxonomy_group__name=resolved_group)
        context[self.variable_name] = taxonomy_item.get_members()
        return ''


register.tag('taxonomy_members', get_taxonomy_members)
