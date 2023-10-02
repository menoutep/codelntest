from rest_framework import permissions

class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Seuls les superutilisateurs peuvent effectuer des modifications, les autres ont un accès en lecture seule
        return request.user and request.user.is_superuser

class IsAuthenticatedUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Seuls les utilisateurs authentifiés peuvent effectuer des modifications sur leur propre objet
        if request.method in permissions.SAFE_METHODS:
            return True  # Les méthodes en lecture seule sont toujours autorisées
        return obj.user == request.user
