from rest_framework import permissions

# Permissions should be in the format "<app label>.<permission codename>".


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsAccountOwner(permissions.BasePermission):
    """
    Custom permission to allow account editing to the respective user only.
    """
    def has_object_permission(self, request, view, account):
        if request.user:
            return account == request.user
        return False
