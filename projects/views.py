from django.shortcuts import render, redirect
from projects.models import Project
from projects.forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from users.models import Profile


@login_required(login_url='user-login')
@permission_required('projects.view_project',raise_exception=True)
def get_projects(request):
    projects_result = Project.objects.filter(owner__user=request.user)
    context = {
        'projects': projects_result
    }
    return render(request, 'projects.html',context)

@login_required(login_url='user-login')
@permission_required('projects.view_project',raise_exception=True)
def get_project(request,project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        print('Project with id {} does not exist.'.format(project_id))
    context = {'project':project}
    projects_visited = request.session.get('projects_visited',[])
    if project_id not in projects_visited:
        projects_visited.append(project_id)
        request.session['projects_visited'] = projects_visited
        
    return render(request, 'project.html', context)

@login_required(login_url='user-login')
@permission_required('projects.add_project',raise_exception=True)
def create_project(request):
    project_form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            try:
                profile = Profile.objects.get(user=request.user)
                project.owner = profile
                project.save()
            except Profile.DoesNotExist:
                print('User profile does not exist')
            return redirect('get-projects')
        else:
            print('errors: ',form.errors)
            return render(request, 'project_form.html',{'form': form})        
    context = {'form':project_form}
    return render(request, 'project_form.html',context)

@login_required(login_url='user-login')
@permission_required('projects.change_project',raise_exception=True)
def edit_project(request,project_id):
    project = Project.objects.get(pk=project_id)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('get-projects')
    context = {'form':form}
    return render(request, 'project_form.html',context)

@login_required(login_url='user-login')
@permission_required('projects.delete_project',raise_exception=True)
def delete_project(request,project_id):
    project = Project.objects.get(pk=project_id)
    
    if request.method == 'POST':
        project.delete()
        return redirect('get-projects')
    context = {'project':project}
    return render(request, 'delete_project.html',context)
    