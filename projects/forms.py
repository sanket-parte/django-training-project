
"""
    How form validation works:
    to_python() -> It converts raw data to python object.
    validate() -> Field specific validation.
    run_validators() -> runs all the validators of field.
"""
from django import forms
from projects.models import Project, Tag
from django.forms import ValidationError


# class ProjectForm(forms.Form):
#     id = forms.UUIDField(max_length=100)
#     title = forms.CharField(widget=forms.Textarea)
#     description = forms.Textarea()
#     source_url = forms.CharField(required=False)
#     demo_link = forms.CharField(required=False)

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'source_url', 'demo_link','tags', 'project_image']
    
   
    def clean(self):
        data = self.cleaned_data
        python_projects = ['Flask Project','Django Project','Bottle Project']
        if data.get('title') in python_projects:
            for tag in data.get('tags'):
                if tag.name not in ['Python']:
                    self.add_error('tags','Selected tag must be Python for forllowing projects: {}' \
                                        .format(','.join(python_projects)))
        super(ProjectForm, self).clean()

    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError('Title should be greater than 5 characters')
        return title
            
    
    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 5:
            raise ValidationError('Description should be greater than 5 characters')
        return description
            
    
