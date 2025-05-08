# decorators.py

from functools import wraps
from django.shortcuts import redirect

def firebase_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated with Firebase
        if not request.user.is_authenticated:
            # Redirect to Firebase login URL or any other page as per your requirement
            return redirect('driver/index.html')  # Replace with your actual Firebase login URL
        return view_func(request, *args, **kwargs)
    return wrapper
