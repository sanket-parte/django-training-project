from django.urls import path
from projects.views import get_projects, get_project, create_project, edit_project, \
    delete_project
from projects.class_based_views import ProjectView, CreateProjectView, UpdateProjectView, \
    DeleteProjectView, ProjectListView, ProjectDetailView, ProjectFormView, TagDetailView

from projects.api.views import get_projects as get_projects_api, get_project as get_project_api, \
                            create_project as create_project_api, update_project as update_project_api, \
                            delete_project as delete_project_api   

from projects.api.rest_framework_views import ProjectView as ProjectViewAPI, ProjectGenericView, \
                            ProjectList, ProjectRetriveUpdateDestroyView
    
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', get_projects, name='get-projects'),
    # path('', login_required(ProjectListView.as_view(), login_url='user-login'), name='get-projects'),
    path('project/<str:project_id>', get_project, name='get-project'),
    # path('project/<str:pk>', ProjectDetailView.as_view(), name='get-project'),
    path('create-project', create_project, name='create-project'),
    # path('create-project', CreateProjectView.as_view(), name='create-project'),
    # path('create-project-form', ProjectFormView.as_view(), name='create-project-form'),
    # path('create-project', CreateProjectView.as_view(), name='create-project'),
    path('edit-project/<str:project_id>', edit_project, name='edit-project'),
    # path('edit-project/<str:project_id>', UpdateProjectView.as_view(), name='edit-project'),
    path('delete-project/<str:project_id>', delete_project, name='delete-project'),
    # path('delete-project/<str:project_id>', DeleteProjectView.as_view(), name='delete-project'),
    path('get-tag/<str:pk>', TagDetailView.as_view(), name='get-tag'),
    # path('api/projects/', get_projects_api),
    path('api/project/', ProjectList.as_view()),
    # path('api/project/<str:project_id>', get_project_api),
    path('api/project/<str:project_id>', ProjectRetriveUpdateDestroyView.as_view()),
    path('api/create-project', create_project_api),
    path('api/update-project', update_project_api),
    path('api/delete-project', delete_project_api),
]
