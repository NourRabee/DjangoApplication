from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


# https://python-code.dev/articles/144154532


class GlobalExceptionsHandler:
    """Handle uncaught exceptions instead of raising a 404."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # Check if the exception is a DoesNotExist exception
        if isinstance(exception, ObjectDoesNotExist):
            # Extract the first word from the exception args as the table name
            table_name = str(exception.args[0]).split()[0]  # Get the first word

            # Customize the message
            error_message = f"{table_name.capitalize()} not found."

            # Show warning in admin using Django messages framework
            messages.warning(request, error_message)

            # Or return JSON for your frontend app
            return JsonResponse({'error': error_message}, status=404)

        return None  # Middlewares should return None when not applied
