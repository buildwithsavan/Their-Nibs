from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def get_user_role(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return 'super_admin'
    if hasattr(user, 'profile'):
        return getattr(user.profile, 'role', 'super_admin')
    return 'catalog_admin' if user.is_staff else 'customer'


def is_staff_or_admin(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    if hasattr(user, 'profile') and getattr(user.profile, 'role', '') in [
        'super_admin', 'catalog_admin', 'order_admin', 'marketing_admin', 'content_admin'
    ]:
        return True
    return False


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"/admin-panel/login/?next={request.path}")
        if not is_staff_or_admin(request.user):
            messages.error(request, "Access denied. Restricted to authorized staff.")
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"/admin-panel/login/?next={request.path}")
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            user_role = get_user_role(request.user)
            if user_role not in allowed_roles and user_role != 'super_admin':
                messages.error(request, f"Permission denied ({', '.join(allowed_roles)} required).")
                return redirect("/admin-panel/dashboard/")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
