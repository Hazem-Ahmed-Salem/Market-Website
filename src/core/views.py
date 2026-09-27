from django.shortcuts import render

def custom_404_view(request, exception=None):
    """
    Global 404 handler that supports custom error messages
    via exception or context.
    """
    message = None
    if exception:
        exc_str = str(exception).strip()
        if exc_str and exc_str.lower() != 'none':
            message = exc_str

    return render(request, '404.html', {'message': message, 'exception': exception}, status=404)
