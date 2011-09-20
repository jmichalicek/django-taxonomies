from django import template

from taxonomy.models import *

register = template.Library()

def get_taxonomy_members(parser, token):
    try:
        bits = tuple(token.split_contents())
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
        # Most examples set variables using template.Variable here
        # and then resolve() in render().  I am doing both in render due to the
        # method call to easily deal with the potential for an arg being
        # a variable or a literal value.
        self.taxonomy_group = taxonomy_group
        self.taxonomy_item = taxonomy_item
        self.variable_name = var_name

    def render(self, context):
        resolved_name = resolve_variable(self.taxonomy_item, context)
        resolved_group = resolve_variable(self.taxonomy_group, context)

        taxonomy_item = TaxonomyItem.objects.get(name=resolved_name,
                                                 taxonomy_group__name=resolved_group)
        context[self.variable_name] = taxonomy_item.get_members()
        return ''

def resolve_variable(arg, context):
    """Attempt to resolve a template param to a template variable value
    or return the param as is if it can't be resolved because it's a real value
    and not a variable"""

    try:
        value = template.Variable(arg).resolve(context)
    except template.VariableDoesNotExist:
        value = arg

    return value

register.tag('taxonomy_members', get_taxonomy_members)
