from rest_framework.response import Response
from rest_framework import serializers

class CustomSuccessResponse(Response):
    def __init__(self, data=None, message=None, status=200, **kwargs):
        resp = {"status": "success", "entity":data, "message":message}
        # resp.update(data)
        super().__init__(data=resp, status=status, **kwargs)


class CustomErrorResponse(Response):
    def __init__(self, data=None, message=None, status=400, **kwargs):
        resp = {"status": "failure", "entity":data, "message":message}
        # resp.update(data)
        super().__init__(data=resp, status=status, **kwargs)


class SerializerCustomErrorResponse(Response):
    def __init__(self, data={}, message=None, status=403, **kwargs):
        resp = {"status": "failure", "entity":data, "message":message}
        
        raise serializers.ValidationError(resp, status)
