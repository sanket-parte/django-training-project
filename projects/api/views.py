import json

from projects.models import Project,Tag,Profile
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from projects.serializers import ProjectSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

@csrf_exempt
@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@csrf_exempt
def get_project(request, project_id):
    response_obj = {}
    if request.method == 'GET':
        try:
            project = Project.objects.get(id=project_id)
        except (ValidationError, Project.DoesNotExist):
            response_obj['error_message'] = 'Supplied project id is not a valid UUID'
            response_obj['status'] = False
            return JsonResponse(response_obj, safe=False)
        serializer = ProjectSerializer(project)
        if serializer.data:
            response_obj['status'] = True
            response_obj['data'] = serializer.data
            response_obj['message'] = 'Projects fetched successfully.'
        else:
            response_obj['status'] = True
            response_obj['data'] = {}
            response_obj['message'] = 'Project with supplied project id does not exist.'
        return JsonResponse(response_obj, safe=False)
    else:
        return JsonResponse({'error_message': 'Invalid HTTP request'}, safe=False)

@csrf_exempt
def create_project(request):
    response_obj = {}
    if request.method == 'POST':
        print('request.body: ',request.body)
        request_body = json.loads(request.body)
        if request_body.get('title') and request_body.get('tags'):
            if not validate_project_tags(request_body.get('tags')):
                return JsonResponse({'error_message': 'Invalid project tags'}, safe=False)
            project = Project()
            project.title = request_body['title']
            project.description = request_body['description']
            project.source_url = request_body['source_url']
            project.demo_link = request_body['demo_link']
            project.project_image = request_body['project_image']
            project.active = request_body['active']
            project.save()
            project.tags.set(request_body['tags'])
            if request_body.get('owner'):
                try:
                    profile = Profile.objects.get(id=request_body['owner'])
                except Profile.DoesNotExist:
                    return JsonResponse({'error_message': 'Invalid project owner'}, safe=False)
                project.owner = profile
            project.save()
            response_obj['status'] = True
            response_obj['message'] = 'Project created successfully.'
            return JsonResponse(response_obj, safe=False)
        else:
            return JsonResponse({'error_message': 'Invalid request object'}, safe=False)
    else:
        return JsonResponse({'error_message': 'Invalid HTTP request'}, safe=False)

@csrf_exempt
def update_project(request):
    response_obj = {}
    if request.method == 'POST':
        request_body = json.loads(request.body)
        if request_body.get('id') and request_body.get('tags'):
            try:
                project = Project.objects.get(id=request_body['id'])
            except Project.DoesNotExist:
                response_obj['status'] = False
                response_obj['message'] = 'Project with id {} does not exist'.format(request_body['id'])
                return JsonResponse(response_obj, safe=False)
            if not validate_project_tags(request_body.get('tags')):
                return JsonResponse({'error_message': 'Invalid project tags'}, safe=False)
            project.title = request_body['title']
            project.description = request_body['description']
            project.source_url = request_body['source_url']
            project.demo_link = request_body['demo_link']
            project.project_image = request_body['project_image']
            project.active = request_body['active']
            project.tags.set(request_body.get('tags'))
            project.save()
            response_obj['status'] = True
            response_obj['message'] = 'Project updated successfully.'
            return JsonResponse(response_obj, safe=False)
        else:
            return JsonResponse({'error_message': 'Invalid request object'}, safe=False)
    else:
        return JsonResponse({'error_message': 'Invalid HTTP request'}, safe=False)

def validate_project_tags(tags):
    for tag_id in tags:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return False
    return True

@csrf_exempt
def delete_project(request):
    response_obj = {}
    if request.method == 'DELETE':
        request_body = json.loads(request.body)
        if request_body.get('id'):
            projects = Project.objects.filter(id=request_body['id'])
            if projects:
                projects.delete()
                response_obj['status'] = True
                response_obj['message'] = 'Project deleted successfully.'
                return JsonResponse(response_obj, safe=False)
            else:
                response_obj['status'] = False
                response_obj['message'] = 'Project with id {} does not exist'.format(request_body['id'])
                return JsonResponse(response_obj, safe=False)
        else:
            return JsonResponse({'error_message': 'Invalid request object'}, safe=False)
    else:
        return JsonResponse({'error_message': 'Invalid HTTP request'}, safe=False)