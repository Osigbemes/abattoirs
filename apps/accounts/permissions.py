from apps.abattoirs.models import Abattoir
from apps.accounts.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.common.responses import CustomErrorResponse, CustomSuccessResponse
from django.core.exceptions import ObjectDoesNotExist

class CustomPermisions:
    def __init__(self, userId):
        self.userId = userId
    
    def create_permission(self, codeName, modelName):
        try:
            user = User.objects.get(id=self.userId)
        except ObjectDoesNotExist:
            return CustomErrorResponse({'Invalid user id':'User does not exist'})
        
        content_type = ContentType.objects.get_for_model(Abattoir)
        permissions_list = Permission.objects.filter(content_type = content_type)
        user_permissions = [permission.codeName for permission in permissions_list]
        # user.user_permissions.set(user_permissions)
        for user_perm in user_permissions:
            user.user_permissions.add(user_perm)
        
        Permission.objects.create(
            codename=codeName,
            name="add_abattoir",
            content_type=content_type
        )
        return permissions_list