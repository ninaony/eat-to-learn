from django.views.decorators.http import require_POST, require_http_methods

@require_POST
def save_recipes_view():
    pass

@require_http_methods(["PATCH"])
def save_recipes_view():
    pass
