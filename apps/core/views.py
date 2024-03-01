from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.cache import cache_page


def health_check(request):
    return HttpResponse("OK")


@cache_page(60 * 15)
def cached(request):
    user_model = get_user_model()
    all_users = user_model.objects.all()
    return HttpResponse(
        "<html><body><h1>{} users.. cached</h1></body></html>".format(
            len(all_users)
        )
    )


def cacheless(request):
    user_model = get_user_model()
    all_users = user_model.objects.all()
    return HttpResponse(
        "<html><body><h1>{} users.. cacheless</h1></body></html>".format(
            len(all_users)
        )
    )
