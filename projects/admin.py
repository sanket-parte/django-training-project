from django.contrib import admin
from projects.models import Project, Review, Tag
from django.utils.html import format_html
from django.urls import reverse
from projects.forms import ProjectForm
from django.contrib import messages    
from datetime import date


class ReviewInline(admin.TabularInline):
    
    model = Review
    fk_name = 'project'
    extra = 0
    verbose_name = 'Project Review'
    
class TagsInline(admin.TabularInline):
    verbose_name = 'Tags'
    model = Project.tags.through
    extra = 0
    
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
        
    form = ProjectForm
    
    inlines = [ReviewInline,TagsInline]
    
    list_display = ['title', 'description', 'tag_list', 'get_full_name','active']
    list_filter = ['tags','owner', 'created_at', 'active']
    search_fields = ('title__startswith','description')
    # fields = ('title', 'description','source_url','demo_link','tags','project_image', \
    #         'owner', 'active')
    actions = ['activate_projects', 'deactivate_projects']
    actions_on_bottom = True
    actions_on_top = True
    
    class Media:
        css = {
            'all':('projects/css/project.css',),
        }
        # js = ('projects/js/project.js',)
    
    fieldsets = (
        ('Details',{
            # 'classes':('collapse',),
            'fields':('title','description','tags','project_image','owner','active')
            }
        ),
        ('Project Links',{
            # 'classes':('collapse',),
            'fields':('source_url','demo_link')
            }
        ),
    )
    
    def get_queryset(self, request):
        qs = super(ProjectAdmin, self).get_queryset(request)
        return qs
    
    def tag_list(self, obj):
        tags = list(obj.tags.all())
        return tags
    tag_list.short_description = 'Project Tags'
    
    def get_full_name(self,obj):
        if obj.owner:
            url = reverse("admin:auth_user_change",kwargs={'object_id':obj.owner.user.id})
            return format_html('<strong><a href="{}">{}</a></strong>',url,obj.owner.user.first_name +' '+ obj.owner.user.last_name)
        return '-'
    get_full_name.short_description = 'Owner Name'
    get_full_name.admin_order_field = 'owner__user__first_name'
    
    @admin.action(description="Activate Projects")
    def activate_projects(self, request, queryset):
        queryset.update(active=True)
        if queryset.count() > 1:
            messages.success(request,'{} projects are activated'.format(queryset.count()))
        else:
            messages.success(request,'Project is activated')
    
    @admin.action(description="Deactivate Projects")
    def deactivate_projects(self, request, queryset):
        queryset.update(active=False)
        if queryset.count() > 1:
            messages.success(request,'{} projects are deactivated'.format(queryset.count()))
        else:
            messages.success(request,'Project is deactivated')

@admin.register(Review) 
class ReviewAdmin(admin.ModelAdmin):
    pass

class ProjectListFilter(admin.SimpleListFilter):
    
    title = 'Project List'
    parameter_name = 'projects'
    
    def lookups(self, request, model_admin):
        projects = Project.objects.filter(active=True).values_list('id','title')
        return projects
    
    def queryset(self, request, queryset):
        project_id = request.GET.get('projects')
        if project_id:
            project = Project.objects.get(id=project_id)
            return project.tags.all()
        return queryset


@admin.register(Tag) 
class TagAdmin(admin.ModelAdmin):
    
    list_display = ['name', 'remarks', 'created_at', 'active']
    list_filter = ['name','created_at', 'active', ProjectListFilter]
    search_fields = ('name__startswith','remarks')