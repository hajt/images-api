from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema

from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from .models import Image
from .serializers import (
    ImageCreateSerializer,
    ImagePartialUpdateSerializer,
    ImageSerializer,
)


class ImagePagination(PageNumberPagination):
    page_size = 10


class ImageFilter(filters.FilterSet):
    class Meta:
        model = Image
        fields = {
            "title": ["icontains"],
        }


class ImageViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = ImagePagination
    http_method_names = ["get", "post", "patch", "delete"]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ImageFilter

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user.id).order_by("title")

    def get_serializer_class(self):
        if self.action == "create":
            serializer = ImageCreateSerializer
        elif self.action == "partial_update":
            serializer = ImagePartialUpdateSerializer
        else:
            serializer = ImageSerializer
        return serializer

    @swagger_auto_schema(responses={HTTP_201_CREATED: ImageSerializer()})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @swagger_auto_schema(responses={HTTP_200_OK: ImageSerializer()})
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
