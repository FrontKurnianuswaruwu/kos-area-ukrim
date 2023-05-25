from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


# function cek login
def login_required():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.session.get('idNama'):
                # Jika pengguna memiliki session userid (sudah login)
                return view_func(request, *args, **kwargs)
            else:
                # Jika pengguna tidak memiliki session userid (belum login)
                messages.error(request, "LOGIN TERLEBIH DAHULU")
                return redirect('login')
        return wrapper
    return decorator