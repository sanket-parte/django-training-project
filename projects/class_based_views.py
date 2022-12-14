from django.shortcuts import render, redirect

from projects.models import Project, Tag
from projects.forms import ProjectForm
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin

class ProjectView(LoginRequiredMixin,PermissionRequiredMixin, View):
    
    permission_required = ('projects.view_project',)
    login_url = 'user-login'
    
    def handle_no_permission(self):
        # add custom message
        # messages.error(self.request, 'You have no permission')
        return super(ProjectView, self).handle_no_permission()
    
    def get(self, request):
        projects_result = Project.objects.all()
        context = {
            'projects': projects_result,
        }
        return render(request, 'projects.html',context)
    
class CreateProjectView(View):
    
    def get(self, request):
        project_form = ProjectForm()
        context = {'form':project_form}
        return render(request, 'project_form.html',context)

    def post(self, request):
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('get-projects')
        return render(request, 'project_form.html',{'form': form})

class UpdateProjectView(View):
    
    def get(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        form = ProjectForm(instance=project)
        context = {'form':form}
        return render(request, 'project_form.html',context)
    
    def post(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('get-projects')
        context = {'form':form}
        return render(request, 'project_form.html',context)

class DeleteProjectView(View):
    
    def get(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        context = {'project':project}
        return render(request, 'delete_project.html',context)
    
    def post(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        project.delete()
        return redirect('get-projects')


class ProjectListView(ListView):
    
    model = Project
    template_name = 'projects.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        queryset = super(ProjectListView, self).get_queryset()
        return queryset.filter()
    
    def get_context_data(self):
        context_data = super(ProjectListView, self).get_context_data()
        context_data.update({
            'projects_description': 'All are python projects.'
        })
        return context_data

class ProjectDetailView(DetailView):
    
    model = Project
    template_name = 'project.html'

class ProjectFormView(FormView):
    
    template_name = 'project_form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('get-projects')
    
    def form_valid(self, form):
        return super().form_valid(form)

class ProjectCreateViewGeneric(CreateView):
    model = Project
    fields =  '__all__'

class TagDetailView(DetailView):
    
    model = Tag
    template_name = 'tag_detail.html'