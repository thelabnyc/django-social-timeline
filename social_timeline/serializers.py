from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Action


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType


class StrRelatedField(serializers.Field):
    def to_representation(self, value):
        return str(value)


class ActionSerializer(serializers.ModelSerializer):
    actor_content_type = ContentTypeSerializer(read_only=True)
    actor = StrRelatedField(read_only=True)
    target_content_type = ContentTypeSerializer(read_only=True)
    target = StrRelatedField(read_only=True)

    class Meta:
        model = Action
        fields = (
            'timestamp', 'target_link', 'target', 'target_object_id',
            'target_content_type', 'verb', 'actor', 'actor_content_type',
            'actor_object_id', 'actor_link',
        )
