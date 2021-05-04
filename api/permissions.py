from rest_framework import permissions

from api.users.groups import Groups


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class BaseGroupPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name=self.group_name).exists():
            return True
        else:
            self.message = f"Permission denied, user not in '{self.group_name}' group"
            return False


class IsEditorPermission(BaseGroupPermissions):
    message = "Must Be Editor"
    group_name = Groups.EDITORS
