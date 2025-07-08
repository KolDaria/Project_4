from django import template

register = template.Library()


@register.filter(name='in_group')
def in_group(user, group_name):
    """
     Checks if a user is in a specific group.
     Usage: {% if user|in_group:"group_name" %}
     """
    return user.groups.filter(name=group_name).exists()
