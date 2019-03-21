from django import template

register = template.Library()

"""
Complete Django Guide part 4 page 38
"""


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    css_class = ''
    # if not isinstance(bound_field, str):
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'

    if field_type(bound_field) == 'Textarea':
        css_class = 'md-textarea'
    return 'form-control {}'.format(css_class)

