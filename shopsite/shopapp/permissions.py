from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''
    Разрешение позволяющее админу удалять, добавлять и изменять запись,
    а остальным только читать
    '''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
 
        return bool(request.user and request.user.is_staff)


