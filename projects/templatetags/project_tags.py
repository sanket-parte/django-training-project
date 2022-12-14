from django import template
from projects.models import Project

register = template.Library()

@register.filter
def convert_to_titlecase(value):
    return value.upper()

@register.filter
def convert_boolean_field(value):
    if value == True:
        return 'Yes'
    else:
        return 'No'

@register.simple_tag
def custom_tag(project_id):
    project = Project.objects.get(id=project_id)
    tags = project.tags.all()
    return tags

@register.inclusion_tag('tags.html', takes_context=True)
def get_project_tags(context,project_id):
    print('project_id: ',project_id)
    # print('context: ',context)
    project = Project.objects.get(id=project_id)
    tags = project.tags.all()
    context['tags'] = tags
    return context

