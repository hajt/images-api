from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "title", "width", "height", "file")
        read_only_fields = ("id", "title", "width", "height", "file")


class ImageCreateSerializer(ImageSerializer):
    class Meta:
        model = Image
        fields = ImageSerializer.Meta.fields
        read_only_fields = ("id",)


class ImagePartialUpdateSerializer(ImageSerializer):
    class Meta:
        model = Image
        fields = ImageSerializer.Meta.fields
        read_only_fields = ("id",)
        extra_kwargs = {
            "title": {"required": False},
            "width": {"required": False},
            "height": {"required": False},
            "file": {"required": False},
        }
