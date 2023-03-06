from combojsonapi.permission.permission_system import PermissionMixin
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user


class IsAuthenticatedPermission(PermissionMixin):
    def get(self, *args, **kwargs):
        if not current_user.is_authenticated:
            raise AccessDenied('No access')
        return super().get(*args, **kwargs)

    def patch_permission(self, *args, **kwargs):
        if not current_user.is_authenticated:
            raise AccessDenied('No access')
        return super().patch_permission(*args, **kwargs)

    def post_permission(self, *args, **kwargs):
        if not current_user.is_authenticated:
            raise AccessDenied('No access')
        return super().patch_permission(*args, **kwargs)

    def delete_permission(self, *args, **kwargs):
        if not current_user.is_authenticated:
            raise AccessDenied('No access')
        return super().patch_permission(*args, **kwargs)
