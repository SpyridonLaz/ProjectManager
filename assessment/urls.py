from django.contrib import admin
from django.urls import path, include

from assessment.apps.manager import urls as manager_urls

"""
===== oAuth2  ======
    Headers:
        Authorization: Basic <base64 encoded client_id:client_secret>
        Content-Type: application/x-www-form-urlencoded
1. Get an access token
    url: /o/token/
    params:
        grant_type=password&username=<username>&password=<password>
3. Refresh an access token 
    url: /o/token/
    params:
        grant_type=refresh_token&refresh_token=<refresh_token>
4. Revoke an access token
    url: /o/revoke_token/
    params:
        revoke_token=<access_token>
        token_type_hint: OPTIONAL, designating either ‘access_token’ or ‘refresh_token’.
python client
    import requests
    requests.Session().auth = ('client_id', 'client_secret')

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include(manager_urls)),

]


from django.views.generic import TemplateView

urlpatterns += [
    # ...
    # Route TemplateView to serve the ReDoc template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
]


from django.views.generic import TemplateView

urlpatterns += [
    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]