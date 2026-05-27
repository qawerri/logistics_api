from rest_framework import permissions


class IsDriverOrReadOnly(permissions.BasePermission):
    """
    Разрешение для событий отслеживания:
    - читать могут все;
    - создавать могут все (для анонимных обновлений статуса);
    - изменять и удалять — только авторизованные пользователи.
    """
    
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'create']:
            return True
        return request.user and request.user.is_authenticated