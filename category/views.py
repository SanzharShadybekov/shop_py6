from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from category import serializers
from category.models import Category


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
