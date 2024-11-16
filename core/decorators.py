from django.http import HttpResponseForbidden

def admin_only(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.role != 'admin':
            return HttpResponseForbidden("You are not authorized to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
