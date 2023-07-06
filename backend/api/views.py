from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import (
    IsProjectOrCreatorOrReadOnly, IsCreator, IsAuthenticated
)
from .serializers import (
    OrganizationViewSerializer, OrganizationCreateSerializer, ProjectSerializer,
    OrganizationUserAddSerializer
)
from tasks.models import Organization, OrganizationUser, Project
from users.models import User


class UserViewSet(DjoserUserViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    
    @action(["get", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)
    


class OrganizationViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    update_permision_classes = (IsCreator,)
    serializer_class = OrganizationViewSerializer
    action_serializers = {
        'retrieve': OrganizationViewSerializer,
        'list': OrganizationViewSerializer,
        'create': OrganizationViewSerializer,
        'partial_update': OrganizationViewSerializer,
        'update': OrganizationUserAddSerializer,
        'delete': OrganizationViewSerializer,
    }

    def get_queryset(self):
        """Возвращает только те Организации, в которых участвует авторизованный 
        пользователь, для администратора - все организации"""
        if self.request.user.is_staff and self.request.user.is_active:
            return Organization.objects.all()
        return Organization.objects.filter(users=self.request.user).all()

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'delete'):
            permission_classes = self.update_permision_classes
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)
        return super(OrganizationViewSet, self).get_serializer_class()
 
    def create(self, request, *args, **kwargs):
        """В этом эндпоинте создается организация, статус владельца 
        автоматически получает авторизованный пользователь."""
        serializer = OrganizationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        organization = Organization.objects.get(title=request.data['title'])
        OrganizationUser.objects.create(
            organization=organization,
            user=request.user,
            role=OrganizationUser.CREATOR,
        )
        serializer = OrganizationViewSerializer(instance=organization)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def retrieve(self, request, *args, **kwargs):
        """В этом эндпоинте можно посмотреть конкретную 
        организацию и ее пользователей."""
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """В этом эндпоинте можно получить весь список 
        организаций авторизованного пользователя."""
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """В этом эндпоинте можно удалить или добавить пользователя в 
        огранизацию. 
         - Для удаления передать булев параметр delete_user.
         - Для добавления пользователя или/и изменения роли 
            передать user: id, role: string.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = self.get_object()
        user = User.objects.get(id=serializer.initial_data.get('user'))
        obj, _ = OrganizationUser.objects.update_or_create(
            organization=organization,
            user=user,
            defaults={'role': serializer.initial_data.get('role')}
        )
        obj.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
    
    def partial_update(self, request, *args, **kwargs):
        """В этом эндпоинте можно переименовать организацию."""
        return super().partial_update(request, *args, **kwargs)
            

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsProjectOrCreatorOrReadOnly]
    serializer_class = ProjectSerializer
