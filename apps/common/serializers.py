from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    status = serializers.CharField()
    data = serializers.DictField(required=False)

class BaseModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        remove_fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if remove_fields:

            for field_name in remove_fields:
                self.fields.pop(field_name)
