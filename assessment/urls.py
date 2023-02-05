from django.contrib import admin
from django.urls import path, include

from  assessment.apps.manager.urls import projects_router, tasks_router
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
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include(projects_router.urls)),
    path('', include(tasks_router.urls)),

]


