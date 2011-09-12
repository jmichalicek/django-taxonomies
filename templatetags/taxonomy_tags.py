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

    if len(bits) == 2:
        #sort of duplicate due to default value on TaxonomyMembers.__init__()
        var_name = "members"
    elif len(bits) == 4 and bits[2] == "as":
        var_name = bits[3]

    return TaxonomyMembers(bits[1], var_name)

class TaxonomyMembers(template.Node):
    def __init__(self, taxonomy_item, var_name="members"):
        self.taxonomy_item_name = template.Variable(taxonomy_item)
        self.variable_name = var_name

    def render(self, context):
        resolved_name = self.taxonomy_item_name.resolve(context)
        taxonomy_item = TaxonomyItem.objects.get(name=resolved_name)
        context[self.variable_name] = taxonomy_item.get_members()
        return ''


register.tag('taxonomy_members', get_taxonomy_members)
