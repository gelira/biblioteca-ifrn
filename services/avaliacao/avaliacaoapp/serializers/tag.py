from rest_framework import serializers

from ..models import Tag

class TagCreateSerializer(serializers.ModelSerializer):
    def validate_tag(self, value):
        return value.upper()

    class Meta:
        model = Tag
        fields = [
            '_id',
            'tag'
        ]
        extra_kwargs = {
            '_id': {
                'read_only': True
            }
        }
