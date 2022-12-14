import uuid
from django.db import models
from users.models import Profile

VOTE_CHOICES = (
    ('up', 'Up Vote'),
    ('down', 'Down Vote'),
)

class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False,max_length=36)
    title = models.CharField('Title', max_length=256, help_text='Enter title for project')
    description = models.TextField('Description', max_length=256, blank=True, null=True,\
                                    help_text='Enter description for project')
    created_at = models.DateTimeField(auto_now_add=True)
    source_url = models.CharField('Source Link', max_length=1200,blank=True, null=True, \
                                help_text='Enter source URL for project')
    demo_link = models.CharField('Demo Link', max_length=1200, blank=True, null=True, \
                                    help_text='Enter demo link for project')
    tags = models.ManyToManyField('Tag', 'Tags', blank=False, help_text='Select tags for project')
    project_image = models.ImageField('Project Image', blank=True,null=True, default='default.jpg', \
                    help_text='Upload project image')
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'project'
        permissions = (('view_projects_visited_count','view projects visited count'),)

class Review(models.Model):
    
    body = models.TextField(max_length=756)
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    total_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.vote}({self.project.title})"
    
    class Meta:
        db_table = 'review'

class Tag(models.Model):
    
    name = models.CharField(max_length=255)
    remarks = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
    