
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, mixins, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from projects.models import Project
from projects.serializers import ProjectSerializer


class ProjectView(APIView):
    '''
    Class based API views using Django REST Framework.
    '''
    
    def get_object(self, project_id):
        try:
            return Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, format=None, *args, **kwargs):
        if kwargs.get('project_id'):
            project = self.get_object(kwargs.get('project_id'))
            serializer = ProjectSerializer(project)
        else:
            serializer = ProjectSerializer(Project.objects.all(), many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, project_id, format=None):
        project = self.get_object(project_id)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, project_id, format=None):
        self.get_object(project_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProjectGenericView(mixins.RetrieveModelMixin,mixins.ListModelMixin, \
            mixins.CreateModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin, \
            generics.GenericAPIView):
    '''
    Class based API views using Django REST Framework Generic API views and Model Mixins.
    '''
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_url_kwarg = 'project_id'
    
    def get_queryset(self):
        queryset = super(ProjectGenericView,self).get_queryset()
        return queryset
    
    def get(self, request, format=None, *args, **kwargs):
        if kwargs.get('project_id'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, format=None, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, format=None, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, format=None, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectList(generics.ListCreateAPIView):
    '''
    Class based API views using Django REST Framework generic API views wrapper.
    '''
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        queryset = super(ProjectList,self).get_queryset()
        return queryset

class ProjectRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Class based API views using Django REST Framework generic API views wrapper.
    '''
    
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_url_kwarg = 'project_id'

    def get(self, request, *args, **kwargs):
        print('request user: ',request.user.user_permissions.all())
        return super(ProjectRetriveUpdateDestroyView, self).get(request, *args, **kwargs)